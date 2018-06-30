from .models import Event, Guild, Response, User


def find_event_from_message(transaction, message_id):
    """Find the event that is associated with the given message id"""
    with transaction.new() as session:
        return session.query(Event).filter_by(message_id=message_id).first()


def find_or_create_response(transaction, user_id, event_id):
    """Find the response with matching user_id and event_id or create one"""
    with transaction.new() as session:
        response = session.query(Response). \
            filter_by(user_id=user_id, event_id=event_id).first()
        if not response:
            response = Response(user_id=user_id, event_id=event_id)
            session.add(response)
    return response


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
