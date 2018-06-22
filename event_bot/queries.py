from .models import Guild, User


def find_or_create_user(transaction, user_id, options=None):
    """Find the user with the given id. If one doesn't exist, create it."""
    return find_or_create_model(transaction, User, user_id, options)


def find_or_create_guild(transaction, guild_id, options=None):
    """Find the guild with the given id. If it doesn't exist, create it."""
    return find_or_create_model(transaction, Guild, guild_id, options)


def find_or_create_model(transaction, Model, model_id, options=None):
    """Find the given model with the given id. If it doesn't exist, create it."""
    with transaction.new() as session:
        if options:
            model = session.query(Model).options(options).filter(Model.id == model_id).first()
        else:
            model = session.query(Model).filter(Model.id == model_id).first()
        if not model:
            model = Model(id=model_id)
            session.add(model)
    return model
