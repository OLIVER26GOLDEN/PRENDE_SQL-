import random
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import data, db
from .schemas import (
    AssistantOut, CertificateCheckRequest, LevelDetail, LevelSummary,
    PracticeRequest, ProgressState, RunRequest, RunResult, TierProgress, UnitOut,
)

app = FastAPI(
    title="SQL Trainer API",
    description="Backend REST API serving the SQL trainer's levels, execution engine and progress logic.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _level_detail(level: dict) -> LevelDetail:
    return LevelDetail.model_validate(level)


@app.get("/api/units", response_model=List[UnitOut])
def list_units():
    return [UnitOut(id=i, **u) for i, u in enumerate(data.UNITS)]


@app.get("/api/levels", response_model=List[LevelSummary])
def list_levels():
    return [LevelSummary(id=l["id"], unit=l["unit"], title=l["title"], free=l["free"]) for l in data.LEVELS]


@app.get("/api/levels/{level_id}", response_model=LevelDetail)
def get_level(level_id: int):
    level = data.get_level(level_id)
    if level is None:
        raise HTTPException(404, "Level not found")
    return _level_detail(level)


@app.post("/api/levels/{level_id}/run", response_model=RunResult)
def run_level(level_id: int, body: RunRequest):
    level = data.get_level(level_id)
    if level is None:
        raise HTTPException(404, "Level not found")

    if not body.sql.strip():
        return RunResult(error="escribe algo primero.")

    conn = db.build_db(level)
    try:
        user_cols, user_rows = db.run_sql(conn, body.sql)
    except db.QueryError as e:
        return RunResult(error=f"error de sintaxis: {e}")

    try:
        expected_cols, expected_rows = db.run_sql(conn, level["expectedSQL"])
    except db.QueryError:
        expected_cols, expected_rows = [], []

    correct = db.results_match(user_cols, user_rows, expected_cols, expected_rows, level["expectedSQL"])
    result = RunResult(
        columns=user_cols,
        rows=db.rows_to_dicts(user_cols, user_rows),
        correct=correct,
    )

    progress = body.progress or ProgressState()

    if body.practice:
        if correct:
            result.xp_gained = 5
            progress.xp += 5
        result.progress = progress
        return result

    if correct:
        if level_id not in progress.completed_levels:
            progress.completed_levels.append(level_id)
            gained = 10 + level_id * 2
            progress.xp += gained
            progress.streak += 1
            result.xp_gained = gained
    else:
        progress.streak = 0

    result.progress = progress
    return result


@app.post("/api/practice/random", response_model=LevelDetail)
def random_practice(body: PracticeRequest):
    pool = body.completed_levels if body.completed_levels else [l["id"] for l in data.LEVELS]
    pool = [i for i in pool if 0 <= i < len(data.LEVELS)]
    if not pool:
        raise HTTPException(400, "No levels available")
    level = data.LEVELS[random.choice(pool)]
    return _level_detail(level)


@app.get("/api/assistant/{level_id}", response_model=AssistantOut)
def assistant(level_id: int):
    level = data.get_level(level_id)
    if level is None:
        raise HTTPException(404, "Level not found")
    return AssistantOut(
        level_id=level_id,
        title=level["title"],
        desc=level["desc"],
        expectedSQL=level["expectedSQL"],
        breakdown=db.build_breakdown(level["expectedSQL"]),
    )


@app.post("/api/certificates/check", response_model=List[TierProgress])
def check_certificates(body: CertificateCheckRequest):
    completed = set(body.completed_levels)
    out = []
    for tier in data.TIERS:
        ids = data.levels_in_tier(tier)
        done_count = sum(1 for i in ids if i in completed)
        out.append(TierProgress(
            key=tier["key"], label=tier["label"], skills=tier["skills"], icon=tier["icon"],
            done_count=done_count, total_count=len(ids), unlocked=done_count == len(ids) and len(ids) > 0,
        ))
    return out


@app.get("/api/health")
def health():
    return {"status": "ok", "levels": len(data.LEVELS)}