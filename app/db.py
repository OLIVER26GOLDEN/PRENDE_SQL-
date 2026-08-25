"""
In-memory SQLite engine used to run both the learner's query and the
expected query for a level, then compare the two result sets.
"""
import json
import re
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class QueryError(Exception):
    """Raised when the user's SQL fails to execute (syntax/semantic error)."""


def _column_type(value: Any) -> str:
    return "INTEGER" if isinstance(value, (int, float)) and not isinstance(value, bool) else "TEXT"


def _build_table(conn: sqlite3.Connection, schema: Dict[str, Any]) -> None:
    rows = schema["rows"]
    if not rows:
        return
    cols = list(rows[0].keys())
    col_defs = ", ".join(f'"{c}" {_column_type(rows[0][c])}' for c in cols)
    table = schema["name"]
    conn.execute(f'DROP TABLE IF EXISTS "{table}";')
    conn.execute(f'CREATE TABLE "{table}" ({col_defs});')
    placeholders = ", ".join(["?"] * len(cols))
    conn.executemany(
        f'INSERT INTO "{table}" VALUES ({placeholders})',
        [tuple(r[c] for c in cols) for r in rows],
    )


def build_db(level: Dict[str, Any]) -> sqlite3.Connection:
    """Create a fresh in-memory SQLite DB seeded with this level's table(s)."""
    conn = sqlite3.connect(":memory:")
    _build_table(conn, level["schema"])
    if "schema2" in level:
        _build_table(conn, level["schema2"])
    return conn


def run_sql(conn: sqlite3.Connection, sql: str) -> Tuple[List[str], List[Tuple]]:
    """Execute arbitrary (learner-supplied) SQL against the sandboxed in-memory DB."""
    try:
        cur = conn.execute(sql)
        columns = [d[0] for d in (cur.description or [])]
        rows = cur.fetchall()
        return columns, rows
    except sqlite3.Error as e:
        raise QueryError(str(e)) from e


def _normalize_rows(columns: List[str], rows: List[Tuple]) -> List[str]:
    """Row -> sorted (col_lower, value) pairs -> JSON string, order-independent on columns."""
    normalized = []
    for row in rows:
        pairs = sorted(
            ((str(c).lower(), v) for c, v in zip(columns, row)),
            key=lambda p: p[0],
        )
        normalized.append(json.dumps(pairs, default=str))
    return normalized


def results_match(
    user_columns: List[str], user_rows: List[Tuple],
    expected_columns: List[str], expected_rows: List[Tuple],
    expected_sql: str,
) -> bool:
    user_norm = _normalize_rows(user_columns, user_rows)
    expected_norm = _normalize_rows(expected_columns, expected_rows)

    if not user_norm or len(user_norm) != len(expected_norm):
        return False

    order_matters = bool(re.search(r"\border\s+by\b", expected_sql, re.IGNORECASE))
    if order_matters:
        return user_norm == expected_norm
    return sorted(user_norm) == sorted(expected_norm)


def rows_to_dicts(columns: List[str], rows: List[Tuple]) -> List[Dict[str, Any]]:
    return [dict(zip(columns, row)) for row in rows]


CLAUSE_EXPLANATIONS: Dict[str, str] = {
    "WITH": "define una subconsulta con nombre (CTE)",
    "SELECT": "elige qué columnas mostrar",
    "FROM": "de qué tabla vienen los datos",
    "LEFT JOIN": "cruza con otra tabla, sin perder filas sin pareja",
    "JOIN": "cruza con otra tabla por una clave en común",
    "WHERE": "filtra filas según una condición",
    "GROUP BY": "agrupa filas que comparten un valor",
    "HAVING": "filtra los grupos ya formados (después de GROUP BY)",
    "PARTITION BY": "agrupa dentro de la ventana, sin fusionar filas",
    "OVER": "función de ventana: calcula algo sin colapsar filas",
    "ORDER BY": "ordena el resultado",
    "LIMIT": "corta el resultado a las primeras N filas",
    "UNION": "apila los resultados de dos SELECT",
}
_CLAUSE_ORDER = list(CLAUSE_EXPLANATIONS.keys())


def build_breakdown(sql: str) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    seen = set()
    for kw in _CLAUSE_ORDER:
        pattern = r"\b" + re.escape(kw).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, sql, re.IGNORECASE) and kw not in seen:
            if kw == "JOIN" and "LEFT JOIN" in seen:
                continue
            found.append({"clause": kw, "explanation": CLAUSE_EXPLANATIONS[kw]})
            seen.add(kw)
    return found