from .models import Guild, User


def find_or_create_user(transaction, id, options=None):
    """Find the user with the given id. If one doesn't exist, create it."""
    return find_or_create_model(transaction, User, id, options)


def find_or_create_guild(transaction, id, options=None):
    """Find the guild with the given id. If it doesn't exist, create it."""
    return find_or_create_model(transaction, Guild, id, options)


def find_or_create_model(transaction, Model, id, options=None):
    """Find the given model with the given id. If it doesn't exist, create it."""
    with transaction.new() as session:
        if options:
            model = session.query(Model).options(options).filter(Model.id == id).first()
        else:
            model = session.query(Model).filter(Model.id == id).first()
        if not model:
            model = Model(id=id)
            session.add(model)
    return model
