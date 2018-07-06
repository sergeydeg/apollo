from contextlib import contextmanager


class DBClient:

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


    def add(self, model):
        """Convenience function for persisting a model"""
        with self.new() as session:
            session.add(model)
