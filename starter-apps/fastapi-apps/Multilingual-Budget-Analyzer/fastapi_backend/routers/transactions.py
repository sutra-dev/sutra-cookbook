from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=List[schemas.TransactionOut])
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Transaction).where(models.Transaction.user_id == current_user.id))
    transactions = result.scalars().all()
    return transactions


@router.post("/", response_model=schemas.TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: schemas.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_tx = models.Transaction(
        user_id=current_user.id,
        amount=transaction_in.amount,
        currency=transaction_in.currency,
        description=transaction_in.description,
        category=transaction_in.category,
        date=transaction_in.date or None,
    )
    db.add(new_tx)
    await db.commit()
    await db.refresh(new_tx)
    return new_tx 