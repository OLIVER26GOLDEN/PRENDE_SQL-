import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=schemas.ProgressOut)
def get_progress(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    progress = db.query(models.Progress).filter(models.Progress.user_id == current_user.id).first()
    if not progress:
        progress = models.Progress(user_id=current_user.id, xp=0, streak=0, completed_levels="[]")
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return schemas.ProgressOut(
        xp=progress.xp,
        streak=progress.streak,
        completed_levels=json.loads(progress.completed_levels or "[]"),
    )


@router.put("", response_model=schemas.ProgressOut)
def update_progress(
    payload: schemas.ProgressUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    progress = db.query(models.Progress).filter(models.Progress.user_id == current_user.id).first()
    if not progress:
        progress = models.Progress(user_id=current_user.id)
        db.add(progress)

    progress.xp = payload.xp
    progress.streak = payload.streak
    progress.completed_levels = json.dumps(payload.completed_levels)
    db.commit()
    db.refresh(progress)

    return schemas.ProgressOut(
        xp=progress.xp,
        streak=progress.streak,
        completed_levels=json.loads(progress.completed_levels or "[]"),
    )
