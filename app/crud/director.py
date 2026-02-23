from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.director import Director
from app.schemas.director import DirectorCreate, DirectorUpdate


class CRUDDirector(CRUDBase[Director, DirectorCreate, DirectorUpdate]):
    pass


crud_director = CRUDDirector(Director)
