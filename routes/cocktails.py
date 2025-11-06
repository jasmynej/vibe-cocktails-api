from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from core.db import get_session
from models import Cocktail

router = APIRouter(prefix="/cocktails", tags=["cocktails"])


@router.get("")
async def get_all_cocktails(session: Session = Depends(get_session)):
    all_cocktails = session.exec(select(Cocktail))
    return all_cocktails.all()
