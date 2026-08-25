"""
Content generator for the SQL trainer.

This is a direct Python port of the JS "DATA GENERATOR" section of the
original single-file app: 10 datasets x 10 concepts = 100 real, runnable
SQL levels, grouped into 10 units, plus 3 certificate tiers.
"""
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Datasets (Sakila / World / Northwind, simplified for teaching purposes)
# ---------------------------------------------------------------------------
DATASETS: List[Dict[str, Any]] = [
    # 1. Sakila - film
    {
        "table": "film", "idCol": "film_id", "nameCol": "title", "nameLabel": "el título",
        "catCol": "rating", "catLabel": "la clasificación", "numCol": "rental_rate",
        "numLabel": "la tarifa de alquiler", "filterCatValue": "G", "filterNumThreshold": 3,
        "rows": [
            {"film_id": 1, "title": "ACADEMY DINOSAUR", "rating": "PG", "rental_rate": 0.99, "length": 86},
            {"film_id": 2, "title": "ACE GOLDFINGER", "rating": "G", "rental_rate": 4.99, "length": 48},
            {"film_id": 3, "title": "ADAPTATION HOLES", "rating": "NC-17", "rental_rate": 2.99, "length": 50},
            {"film_id": 4, "title": "AFFAIR PREJUDICE", "rating": "G", "rental_rate": 1.99, "length": 117},
        ],
        "second": {
            "table": "category", "fkCol": "film_id", "labelCol": "name", "labelLabel": "la categoría",
            "rows": [
                {"category_id": 1, "film_id": 1, "name": "Documentary"},
                {"category_id": 2, "film_id": 2, "name": "Horror"},
                {"category_id": 3, "film_id": 4, "name": "Comedy"},
            ],
        },
    },
    # 2. Sakila - payment
    {
        "table": "payment", "idCol": "payment_id", "nameCol": "payment_date", "nameLabel": "la fecha de pago",
        "catCol": "staff_name", "catLabel": "el empleado que gestionó el pago", "numCol": "amount",
        "numLabel": "el importe", "filterCatValue": "Mike Hillyer", "filterNumThreshold": 5,
        "rows": [
            {"payment_id": 1, "payment_date": "2023-01-24", "staff_name": "Mike Hillyer", "amount": 2.99},
            {"payment_id": 2, "payment_date": "2023-01-25", "staff_name": "Mike Hillyer", "amount": 7.99},
            {"payment_id": 3, "payment_date": "2023-01-26", "staff_name": "Jon Stephens", "amount": 1.99},
            {"payment_id": 4, "payment_date": "2023-01-27", "staff_name": "Jon Stephens", "amount": 9.99},
        ],
        "second": {
            "table": "customer", "fkCol": "payment_id", "labelCol": "first_name", "labelLabel": "el cliente",
            "rows": [
                {"customer_id": 1, "payment_id": 1, "first_name": "Mary"},
                {"customer_id": 2, "payment_id": 2, "first_name": "Patricia"},
                {"customer_id": 3, "payment_id": 4, "first_name": "Linda"},
            ],
        },
    },
    # 3. Sakila - film_list
    {
        "table": "film_list", "idCol": "FID", "nameCol": "title", "nameLabel": "el título",
        "catCol": "category", "catLabel": "la categoría", "numCol": "price", "numLabel": "el precio",
        "filterCatValue": "Comedy", "filterNumThreshold": 3,
        "rows": [
            {"FID": 1, "title": "ACADEMY DINOSAUR", "category": "Documentary", "price": 0.99, "rating": "PG"},
            {"FID": 2, "title": "ACE GOLDFINGER", "category": "Horror", "price": 3.99, "rating": "G"},
            {"FID": 3, "title": "AFRICAN EGG", "category": "Family", "price": 1.99, "rating": "G"},
            {"FID": 4, "title": "AGENT TRUMAN", "category": "Comedy", "price": 2.99, "rating": "PG"},
            {"FID": 5, "title": "ALI FOREVER", "category": "Comedy", "price": 4.99, "rating": "PG"},
        ],
        "second": {
            "table": "actor", "fkCol": "FID", "labelCol": "actor_name", "labelLabel": "el actor",
            "rows": [
                {"actor_id": 1, "FID": 2, "actor_name": "PENELOPE GUINESS"},
                {"actor_id": 2, "FID": 4, "actor_name": "NICK WAHLBERG"},
                {"actor_id": 3, "FID": 5, "actor_name": "ED CHASE"},
            ],
        },
    },
    # 4. World - country
    {
        "table": "country", "idCol": "Code", "nameCol": "Name", "nameLabel": "el nombre",
        "catCol": "Continent", "catLabel": "el continente", "numCol": "Population",
        "numLabel": "la población", "filterCatValue": "Europe", "filterNumThreshold": 40000000,
        "rows": [
            {"Code": "ESP", "Name": "Spain", "Continent": "Europe", "Population": 46754784},
            {"Code": "PRT", "Name": "Portugal", "Continent": "Europe", "Population": 9918040},
            {"Code": "MEX", "Name": "Mexico", "Continent": "North America", "Population": 98881000},
            {"Code": "ARG", "Name": "Argentina", "Continent": "South America", "Population": 37032000},
        ],
        "second": {
            "table": "city", "fkCol": "CountryCode", "labelCol": "Name", "labelLabel": "la ciudad",
            "rows": [
                {"ID": 1, "Name": "Madrid", "CountryCode": "ESP"},
                {"ID": 2, "Name": "Buenos Aires", "CountryCode": "ARG"},
                {"ID": 3, "Name": "Mexico City", "CountryCode": "MEX"},
            ],
        },
    },
    # 5. World - city
    {
        "table": "city", "idCol": "CountryCode", "nameCol": "Name", "nameLabel": "el nombre",
        "catCol": "CountryCode", "catLabel": "el código de país", "numCol": "Population",
        "numLabel": "la población", "filterCatValue": "ESP", "filterNumThreshold": 1000000,
        "rows": [
            {"ID": 1, "Name": "Madrid", "CountryCode": "ESP", "Population": 3223000},
            {"ID": 2, "Name": "Barcelona", "CountryCode": "ESP", "Population": 1620000},
            {"ID": 3, "Name": "Lisbon", "CountryCode": "PRT", "Population": 505000},
            {"ID": 4, "Name": "Porto", "CountryCode": "PRT", "Population": 237000},
        ],
        "second": {
            "table": "countrylanguage", "fkCol": "CountryCode", "labelCol": "Language", "labelLabel": "el idioma",
            "rows": [
                {"id": 1, "CountryCode": "ESP", "Language": "Spanish"},
                {"id": 2, "CountryCode": "PRT", "Language": "Portuguese"},
            ],
        },
    },
    # 6. World - countrylanguage
    {
        "table": "countrylanguage", "idCol": "CountryCode", "nameCol": "Language", "nameLabel": "el idioma",
        "catCol": "IsOfficial", "catLabel": "si es oficial", "numCol": "Percentage",
        "numLabel": "el porcentaje de hablantes", "filterCatValue": "T", "filterNumThreshold": 50,
        "rows": [
            {"id": 1, "CountryCode": "ESP", "Language": "Spanish", "IsOfficial": "T", "Percentage": 74.4},
            {"id": 2, "CountryCode": "ESP", "Language": "Catalan", "IsOfficial": "F", "Percentage": 16.9},
            {"id": 3, "CountryCode": "MEX", "Language": "Spanish", "IsOfficial": "T", "Percentage": 92.7},
            {"id": 4, "CountryCode": "ARG", "Language": "Spanish", "IsOfficial": "T", "Percentage": 96.8},
        ],
        "second": {
            "table": "country", "fkCol": "CountryCode", "labelCol": "Name", "labelLabel": "el país",
            "rows": [
                {"id": 1, "CountryCode": "ESP", "Name": "Spain"},
                {"id": 2, "CountryCode": "MEX", "Name": "Mexico"},
            ],
        },
    },
    # 7. Northwind - products
    {
        "table": "products", "idCol": "ProductID", "nameCol": "ProductName", "nameLabel": "el nombre",
        "catCol": "CategoryName", "catLabel": "la categoría", "numCol": "UnitPrice",
        "numLabel": "el precio unitario", "filterCatValue": "Beverages", "filterNumThreshold": 15,
        "rows": [
            {"ProductID": 1, "ProductName": "Chai", "CategoryName": "Beverages", "UnitPrice": 18.00},
            {"ProductID": 2, "ProductName": "Chang", "CategoryName": "Beverages", "UnitPrice": 19.00},
            {"ProductID": 3, "ProductName": "Aniseed Syrup", "CategoryName": "Condiments", "UnitPrice": 10.00},
            {"ProductID": 4, "ProductName": "Chef Anton's Cajun Seasoning", "CategoryName": "Condiments", "UnitPrice": 22.00},
        ],
        "second": {
            "table": "order_details", "fkCol": "ProductID", "labelCol": "Quantity", "labelLabel": "la cantidad pedida",
            "rows": [
                {"id": 1, "ProductID": 1, "Quantity": 10},
                {"id": 2, "ProductID": 2, "Quantity": 5},
                {"id": 3, "ProductID": 4, "Quantity": 20},
            ],
        },
    },
    # 8. Northwind - orders
    {
        "table": "orders", "idCol": "OrderID", "nameCol": "OrderDate", "nameLabel": "la fecha del pedido",
        "catCol": "ShipCountry", "catLabel": "el país de envío", "numCol": "Freight",
        "numLabel": "el coste de envío", "filterCatValue": "Germany", "filterNumThreshold": 50,
        "rows": [
            {"OrderID": 10248, "OrderDate": "1996-07-04", "ShipCountry": "France", "Freight": 32.38},
            {"OrderID": 10249, "OrderDate": "1996-07-05", "ShipCountry": "Germany", "Freight": 11.61},
            {"OrderID": 10250, "OrderDate": "1996-07-08", "ShipCountry": "Germany", "Freight": 65.83},
            {"OrderID": 10251, "OrderDate": "1996-07-08", "ShipCountry": "France", "Freight": 41.34},
        ],
        "second": {
            "table": "customers", "fkCol": "OrderID", "labelCol": "CompanyName", "labelLabel": "el cliente",
            "rows": [
                {"id": 1, "OrderID": 10248, "CompanyName": "Vins et alcools Chevalier"},
                {"id": 2, "OrderID": 10249, "CompanyName": "Toms Spezialitäten"},
                {"id": 3, "OrderID": 10251, "CompanyName": "Victuailles en stock"},
            ],
        },
    },
    # 9. Northwind - employees
    {
        "table": "employees", "idCol": "EmployeeID", "nameCol": "LastName", "nameLabel": "el apellido",
        "catCol": "Title", "catLabel": "el puesto", "numCol": "YearsOfService",
        "numLabel": "los años de servicio", "filterCatValue": "Sales Representative", "filterNumThreshold": 3,
        "rows": [
            {"EmployeeID": 1, "LastName": "Davolio", "Title": "Sales Representative", "YearsOfService": 5},
            {"EmployeeID": 2, "LastName": "Fuller", "Title": "Sales Manager", "YearsOfService": 8},
            {"EmployeeID": 3, "LastName": "Leverling", "Title": "Sales Representative", "YearsOfService": 2},
            {"EmployeeID": 4, "LastName": "Peacock", "Title": "Sales Representative", "YearsOfService": 6},
        ],
        "second": {
            "table": "orders", "fkCol": "EmployeeID", "labelCol": "ShipCountry", "labelLabel": "el país del pedido",
            "rows": [
                {"id": 1, "EmployeeID": 1, "ShipCountry": "France"},
                {"id": 2, "EmployeeID": 2, "ShipCountry": "Germany"},
                {"id": 3, "EmployeeID": 4, "ShipCountry": "Brazil"},
            ],
        },
    },
    # 10. Sakila - rental
    {
        "table": "rental", "idCol": "rental_id", "nameCol": "rental_date", "nameLabel": "la fecha de alquiler",
        "catCol": "staff_name", "catLabel": "el empleado", "numCol": "days_rented",
        "numLabel": "los días alquilados", "filterCatValue": "Mike Hillyer", "filterNumThreshold": 3,
        "rows": [
            {"rental_id": 1, "rental_date": "2023-02-01", "staff_name": "Mike Hillyer", "days_rented": 5},
            {"rental_id": 2, "rental_date": "2023-02-02", "staff_name": "Mike Hillyer", "days_rented": 2},
            {"rental_id": 3, "rental_date": "2023-02-03", "staff_name": "Jon Stephens", "days_rented": 7},
            {"rental_id": 4, "rental_date": "2023-02-04", "staff_name": "Jon Stephens", "days_rented": 1},
        ],
        "second": {
            "table": "customer", "fkCol": "rental_id", "labelCol": "first_name", "labelLabel": "el cliente",
            "rows": [
                {"customer_id": 1, "rental_id": 1, "first_name": "Mary"},
                {"customer_id": 2, "rental_id": 3, "first_name": "Patricia"},
                {"customer_id": 3, "rental_id": 4, "first_name": "Mary"},
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# Concept (exercise) generators - one per unit
# ---------------------------------------------------------------------------
def _concept_select(ds):
    return {
        "title": "SELECT básico",
        "desc": f"Quiere ver {ds['nameLabel']} y {ds['catLabel']} de todos los registros de la tabla <b>{ds['table']}</b>.",
        "hintText": f"Necesitas <code>SELECT</code> para elegir columnas (<code>{ds['nameCol']}, {ds['catCol']}</code>) y <code>FROM {ds['table']}</code>.",
        "expectedSQL": f"SELECT {ds['nameCol']}, {ds['catCol']} FROM {ds['table']}",
    }


def _concept_where(ds):
    return {
        "title": "WHERE + condición",
        "desc": f"Filtra: quiere solo los registros donde {ds['catLabel']} sea <b>{ds['filterCatValue']}</b> y {ds['numLabel']} sea mayor que <b>{ds['filterNumThreshold']}</b>.",
        "hintText": f"Necesitas <code>WHERE</code> con dos condiciones unidas por <code>AND</code>: <code>{ds['catCol']} = '{ds['filterCatValue']}'</code> y <code>{ds['numCol']} > {ds['filterNumThreshold']}</code>.",
        "expectedSQL": f"SELECT * FROM {ds['table']} WHERE {ds['catCol']} = '{ds['filterCatValue']}' AND {ds['numCol']} > {ds['filterNumThreshold']}",
    }


def _concept_order_limit(ds):
    return {
        "title": "ORDER BY + LIMIT",
        "desc": f"Saca los <b>2</b> registros con {ds['numLabel']} más alto, de mayor a menor.",
        "hintText": f"Ordena con <code>ORDER BY {ds['numCol']} DESC</code> y corta con <code>LIMIT 2</code>.",
        "expectedSQL": f"SELECT * FROM {ds['table']} ORDER BY {ds['numCol']} DESC LIMIT 2",
    }


def _concept_group_avg(ds):
    return {
        "title": "GROUP BY y agregación",
        "desc": f"Calcula {ds['numLabel']} medio (<b>media</b>) agrupado por {ds['catLabel']}.",
        "hintText": f"Necesitas <code>GROUP BY {ds['catCol']}</code> y <code>AVG({ds['numCol']}) AS media</code>.",
        "expectedSQL": f"SELECT {ds['catCol']}, AVG({ds['numCol']}) AS media FROM {ds['table']} GROUP BY {ds['catCol']}",
    }


def _concept_having(ds):
    return {
        "title": "HAVING",
        "desc": f"Encuentra los valores de {ds['catLabel']} que aparecen en <b>más de un</b> registro.",
        "hintText": "<code>WHERE</code> filtra antes de agrupar; <code>HAVING</code> filtra después. Usa <code>HAVING COUNT(*) > 1</code>.",
        "expectedSQL": f"SELECT {ds['catCol']}, COUNT(*) AS total FROM {ds['table']} GROUP BY {ds['catCol']} HAVING COUNT(*) > 1",
    }


def _join_select_cols(ds):
    collide = ds["nameCol"].lower() == ds["second"]["labelCol"].lower()
    if not collide:
        cols = f"t.{ds['nameCol']}, s.{ds['second']['labelCol']}"
        return cols, cols
    alias1 = f"{ds['table']}_{ds['nameCol']}"
    alias2 = f"{ds['second']['table']}_{ds['second']['labelCol']}"
    sql = f"t.{ds['nameCol']} AS {alias1}, s.{ds['second']['labelCol']} AS {alias2}"
    return sql, sql


def _concept_join(ds):
    cols_sql, cols_hint = _join_select_cols(ds)
    return {
        "title": "JOIN entre tablas",
        "desc": f"Cruza <b>{ds['table']}</b> con <b>{ds['second']['table']}</b> para ver {ds['nameLabel']} junto a {ds['second']['labelLabel']}.",
        "hintText": f"<code>SELECT {cols_hint} FROM {ds['table']} t JOIN {ds['second']['table']} s ON t.{ds['idCol']} = s.{ds['second']['fkCol']}</code>.",
        "expectedSQL": f"SELECT {cols_sql} FROM {ds['table']} t JOIN {ds['second']['table']} s ON t.{ds['idCol']} = s.{ds['second']['fkCol']}",
        "needsSecond": True,
    }


def _concept_left_join(ds):
    cols_sql, cols_hint = _join_select_cols(ds)
    return {
        "title": "LEFT JOIN",
        "desc": f"Lista <b>todos</b> los registros de {ds['table']} y su dato relacionado en {ds['second']['table']} (si no tiene, que aparezca con NULL).",
        "hintText": f"Un <code>JOIN</code> normal descarta los que no tienen relación. Usa <code>LEFT JOIN</code> para conservarlos todos. <code>SELECT {cols_hint} FROM {ds['table']} t LEFT JOIN {ds['second']['table']} s ON t.{ds['idCol']} = s.{ds['second']['fkCol']}</code>.",
        "expectedSQL": f"SELECT {cols_sql} FROM {ds['table']} t LEFT JOIN {ds['second']['table']} s ON t.{ds['idCol']} = s.{ds['second']['fkCol']}",
        "needsSecond": True,
    }


def _concept_subquery(ds):
    return {
        "title": "Subconsultas",
        "desc": f"Encuentra los registros donde {ds['numLabel']} es <b>mayor que la media</b> de todos.",
        "hintText": f"<code>WHERE {ds['numCol']} > (SELECT AVG({ds['numCol']}) FROM {ds['table']})</code>.",
        "expectedSQL": f"SELECT * FROM {ds['table']} WHERE {ds['numCol']} > (SELECT AVG({ds['numCol']}) FROM {ds['table']})",
    }


def _concept_cte(ds):
    return {
        "title": "CTE (WITH)",
        "desc": "Reescribe la consulta de la media usando un <b>CTE</b> en vez de una subconsulta suelta.",
        "hintText": f"<code>WITH media AS (SELECT AVG({ds['numCol']}) AS m FROM {ds['table']}) SELECT ...</code>.",
        "expectedSQL": f"WITH media AS (SELECT AVG({ds['numCol']}) AS m FROM {ds['table']}) SELECT * FROM {ds['table']} WHERE {ds['numCol']} > (SELECT m FROM media)",
    }


def _concept_window(ds, idx):
    if idx % 2 == 0:
        return {
            "title": "Window: ROW_NUMBER 🏆",
            "desc": f"Asigna a cada registro un <b>puesto (posicion)</b> dentro de {ds['catLabel']}, según {ds['numLabel']} de mayor a menor.",
            "hintText": f"<code>ROW_NUMBER() OVER (PARTITION BY {ds['catCol']} ORDER BY {ds['numCol']} DESC) AS posicion</code>.",
            "expectedSQL": f"SELECT *, ROW_NUMBER() OVER (PARTITION BY {ds['catCol']} ORDER BY {ds['numCol']} DESC) AS posicion FROM {ds['table']}",
        }
    return {
        "title": "Window: acumulado 🏆",
        "desc": f"Ordena por {ds['numLabel']} ascendente y calcula el <b>acumulado</b> (running total).",
        "hintText": f"<code>SUM({ds['numCol']}) OVER (ORDER BY {ds['numCol']}) AS acumulado</code> — el ORDER BY va dentro del OVER.",
        "expectedSQL": f"SELECT *, SUM({ds['numCol']}) OVER (ORDER BY {ds['numCol']}) AS acumulado FROM {ds['table']} ORDER BY {ds['numCol']}",
    }


CONCEPT_FNS = [
    _concept_select, _concept_where, _concept_order_limit, _concept_group_avg, _concept_having,
    _concept_join, _concept_left_join, _concept_subquery, _concept_cte, _concept_window,
]


# ---------------------------------------------------------------------------
# Units (10) - metadata + intro text shown before each unit's first level
# ---------------------------------------------------------------------------
UNITS: List[Dict[str, str]] = [
    {"icon": "📖", "name": "Fundamentos", "desc": "SELECT — elegir columnas.", "accent": "#3DDC97", "accent2": "#1E7A54",
     "intro": "<b>SELECT</b> es la instrucción básica para leer datos: le dices qué columnas quieres ver y de qué tabla."},
    {"icon": "🧮", "name": "Filtros", "desc": "WHERE — quedarte solo con lo que importa.", "accent": "#4FC3F7", "accent2": "#1B6B8C",
     "intro": "<b>WHERE</b> filtra filas: solo se quedan las que cumplen una condición."},
    {"icon": "📐", "name": "Orden y límites", "desc": "ORDER BY, LIMIT — ranking de resultados.", "accent": "#7C8CFF", "accent2": "#3B45A0",
     "intro": "<b>ORDER BY</b> ordena el resultado por una columna. <b>LIMIT</b> corta el resultado a las primeras N filas."},
    {"icon": "📊", "name": "Agregación", "desc": "GROUP BY — resumir datos por categoría.", "accent": "#C792EA", "accent2": "#6B3FA0",
     "intro": "<b>GROUP BY</b> agrupa filas con funciones de agregación como AVG(), SUM(), COUNT()."},
    {"icon": "🎯", "name": "Refinar grupos", "desc": "HAVING — filtrar después de agrupar.", "accent": "#FF8AD8", "accent2": "#A03B7E",
     "intro": "<b>HAVING</b> es como <code>WHERE</code>, pero para usar después de un <code>GROUP BY</code>."},
    {"icon": "🔗", "name": "Relaciones", "desc": "JOIN — cruzar tablas distintas.", "accent": "#FF6FA5", "accent2": "#A03B65",
     "intro": "<b>JOIN</b> combina filas de dos tablas relacionadas mediante una columna en común."},
    {"icon": "🧩", "name": "Relaciones completas", "desc": "LEFT JOIN — no perder registros sin relación.", "accent": "#FFB454", "accent2": "#B36A1E",
     "intro": "<b>LEFT JOIN</b> conserva todas las filas de la primera tabla aunque no tengan pareja en la segunda."},
    {"icon": "🧠", "name": "Subconsultas", "desc": "Una query dentro de otra.", "accent": "#FFD166", "accent2": "#B38A1E",
     "intro": "Una <b>subconsulta</b> es un SELECT metido dentro de otra consulta, entre paréntesis."},
    {"icon": "🪄", "name": "CTEs", "desc": "WITH — queries complejas legibles.", "accent": "#F76E6E", "accent2": "#A03B3B",
     "intro": "Un <b>CTE</b> (WITH) es una subconsulta con nombre, usada como si fuera una tabla temporal."},
    {"icon": "🏆", "name": "Nivel profesional", "desc": "Window functions — lo que piden en entrevistas reales.", "accent": "#FFD700", "accent2": "#B8860B",
     "intro": "Las <b>window functions</b> calculan algo sin colapsar las filas como hace GROUP BY."},
]


# ---------------------------------------------------------------------------
# Certificate tiers
# ---------------------------------------------------------------------------
TIERS: List[Dict[str, Any]] = [
    {"key": "basico", "label": "Nivel Básico", "unitsFrom": 0, "unitsTo": 2,
     "skills": "SELECT, WHERE, ORDER BY y LIMIT", "icon": "🌱"},
    {"key": "medio", "label": "Nivel Intermedio", "unitsFrom": 3, "unitsTo": 6,
     "skills": "GROUP BY, HAVING, JOIN y LEFT JOIN", "icon": "⚙️"},
    {"key": "pro", "label": "Nivel Profesional", "unitsFrom": 7, "unitsTo": 9,
     "skills": "Subconsultas, CTEs y window functions", "icon": "🏆"},
]


def _build_levels() -> List[Dict[str, Any]]:
    levels: List[Dict[str, Any]] = []
    for c_idx, fn in enumerate(CONCEPT_FNS):
        for d_idx, ds in enumerate(DATASETS):
            base = fn(ds, d_idx) if fn is _concept_window else fn(ds)
            level = {
                "id": len(levels),
                "unit": c_idx,
                "title": base["title"],
                "desc": base["desc"],
                "hintText": base["hintText"],
                "schema": {"name": ds["table"], "rows": ds["rows"]},
                "expectedSQL": base["expectedSQL"],
                "free": False,
            }
            if base.get("needsSecond"):
                level["schema2"] = {"name": ds["second"]["table"], "rows": ds["second"]["rows"]}
            levels.append(level)
    levels[0]["free"] = True
    levels[1]["free"] = True
    return levels


LEVELS: List[Dict[str, Any]] = _build_levels()


def get_level(level_id: int) -> Optional[Dict[str, Any]]:
    if 0 <= level_id < len(LEVELS):
        return LEVELS[level_id]
    return None


def levels_in_tier(tier: Dict[str, Any]) -> List[int]:
    return [l["id"] for l in LEVELS if tier["unitsFrom"] <= l["unit"] <= tier["unitsTo"]]