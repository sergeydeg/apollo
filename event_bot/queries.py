from .models import Guild, User


def find_or_create_user(session_scope, id):
    """Find the user with the given id. If one doesn't exist, create it."""
    return find_or_create_model(session_scope, User, id) 


def find_or_create_guild(session_scope, id):
    """Find the guild with the given id. If it doesn't exist, create it."""
    return find_or_create_model(session_scope, Guild, id) 


def find_or_create_model(session_scope, Model, id):
    """Find the given model with the given id. If it doesn't exist, create it."""
    with session_scope.new() as session:
        model = session.query(Model).filter(Model.id == id).first()
        if not model:
            model = Model(id=id)
            session.add(model)
    return model
