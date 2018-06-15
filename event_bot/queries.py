from .models import Guild, User


def find_or_create_user(transaction, id):
    """Find the user with the given id. If one doesn't exist, create it."""
    return find_or_create_model(transaction, User, id) 


def find_or_create_guild(transaction, id):
    """Find the guild with the given id. If it doesn't exist, create it."""
    return find_or_create_model(transaction, Guild, id) 


def find_or_create_model(transaction, Model, id):
    """Find the given model with the given id. If it doesn't exist, create it."""
    with transaction.new() as session:
        model = session.query(Model).filter(Model.id == id).first()
        if not model:
            model = Model(id=id)
            session.add(model)
    return model
