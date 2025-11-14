from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from uuid import UUID

async def create_task(db: AsyncSession, task_in: schemas.TaskCreate):
    task = models.Task(**task_in.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Task).offset(skip).limit(limit))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: UUID):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task_id: UUID, task_in: schemas.TaskUpdate):
    task = await get_task(db, task_id)
    if not task:
        return None
    for key, value in task_in.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task_id: UUID):
    task = await get_task(db, task_id)
    if not task:
        return False
    await db.delete(task)
    await db.commit()
    return True
