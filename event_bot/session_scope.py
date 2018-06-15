from contextlib import contextmanager


class SessionScope:

    def __init__(self, Session):
        self.Session = Session


    @contextmanager
    def new(self):
        """Provide a transactional scope around a series of DB operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
