from contextlib import contextmanager


class Transaction:

    def __init__(self, session):
        self.session = session


    @contextmanager
    def new(self):
        """Provide a transactional scope around a series of DB operations"""
        try:
            yield self.session
            self.session.commit()
        except:
            self.session.rollback()
            raise
