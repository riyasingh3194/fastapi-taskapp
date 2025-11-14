from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
async def create_task(task_in: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task_in)

@router.get("/", response_model=List[schemas.TaskOut])
async def list_tasks(page: int = Query(1), per_page: int = Query(10), db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * per_page
    return await crud.get_tasks(db, skip, per_page)

@router.patch("/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: UUID, task_in: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await crud.update_task(db, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Deleted successfully"}
