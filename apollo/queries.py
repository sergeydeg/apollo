from sqlalchemy.orm import joinedload

from .models import Event, EventChannel, Guild, Response, User


def find_event_channel(session, event_channel_id):
    return session.query(EventChannel). \
        options(joinedload('events').joinedload('responses')). \
        filter_by(id=event_channel_id). \
        first()


def find_event(session, event_id):
    return session.query(Event). \
        options(joinedload('event_channel')). \
        options(joinedload('responses')). \
        filter_by(id=event_id). \
        first()


def find_event_from_message(session, message_id):
    return session.query(Event).filter_by(message_id=message_id).first()


def find_response(session, user_id, event_id):
    return session.query(Response). \
        filter_by(event_id=event_id, user_id=user_id). \
        first()


def find_or_create_user(session, user_id):
    return find_or_create_model(session, User, user_id)


def find_or_create_guild(session, guild_id):
    return find_or_create_model(session, Guild, guild_id)


def find_or_create_model(session, Model, model_id):
    model = session.query(Model).filter(Model.id == model_id).first()
    if not model:
        model = Model(id=model_id)
        session.add(model)
    return model
