from contextlib import contextmanager


class ScopedSession:
    def __init__(self, build_session):
        self.build_session = build_session

    @contextmanager
    def call(self):
        session = self.build_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
