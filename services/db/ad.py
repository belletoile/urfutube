from sqlalchemy.orm import Session

from models.models import Ad
from schemas.ad import AdBaseSchema


def create_ad(session: Session, ad: AdBaseSchema):
    db_ad = Ad(**ad.dict())
    session.add(db_ad)
    session.commit()
    session.refresh(db_ad)
    return db_ad
