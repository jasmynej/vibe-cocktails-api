from sqlmodel import Session, select

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, instance):
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, model, model_id: int):
        return self.session.get(model, model_id)


