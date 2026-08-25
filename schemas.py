from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SchemaTable(BaseModel):
    name: str
    rows: List[Dict[str, Any]]


class UnitOut(BaseModel):
    id: int
    icon: str
    name: str
    desc: str
    accent: str
    accent2: str
    intro: str


class LevelSummary(BaseModel):
    id: int
    unit: int
    title: str
    free: bool


class LevelDetail(BaseModel):
    id: int
    unit: int
    title: str
    desc: str
    hintText: str
    schema_: SchemaTable = Field(alias="schema")
    schema2: Optional[SchemaTable] = None
    expectedSQL: str
    free: bool

    class Config:
        populate_by_name = True


class ProgressState(BaseModel):
    completed_levels: List[int] = []
    xp: int = 0
    streak: int = 0


class RunRequest(BaseModel):
    sql: str
    progress: Optional[ProgressState] = None
    practice: bool = False


class RunResult(BaseModel):
    columns: List[str] = []
    rows: List[Dict[str, Any]] = []
    correct: bool = False
    error: Optional[str] = None
    xp_gained: int = 0
    progress: Optional[ProgressState] = None


class PracticeRequest(BaseModel):
    completed_levels: List[int] = []


class AssistantOut(BaseModel):
    level_id: int
    title: str
    desc: str
    expectedSQL: str
    breakdown: List[Dict[str, str]]


class TierProgress(BaseModel):
    key: str
    label: str
    skills: str
    icon: str
    done_count: int
    total_count: int
    unlocked: bool


class CertificateCheckRequest(BaseModel):
    completed_levels: List[int] = []