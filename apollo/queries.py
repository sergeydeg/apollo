from sqlalchemy import exists, func
from sqlalchemy.orm import joinedload

from .models import Event, EventChannel, Guild, Response, User


def event_count_for_event_channel(session, event_channel_id):
    return _get_count(session.query(Event).filter_by(event_channel_id=event_channel_id))


def event_channel_count_for_guild(session, guild_id):
    return _get_count(session.query(EventChannel).filter_by(guild_id=guild_id))


def total_user_count(session):
    return _get_count(session.query(User))


def total_event_count(session):
    return _get_count(session.query(Event))


def event_channel_exists(session, event_channel_id):
    return session.query(exists().where(EventChannel.id == event_channel_id)).scalar()


def find_event_channel(session, event_channel_id):
    return session.query(EventChannel).filter_by(id=event_channel_id).first()


def find_event_from_message(session, message_id):
    return session.query(Event).filter_by(message_id=message_id).first()


def find_response(session, user_id, event_id):
    return session.query(Response).filter_by(event_id=event_id, user_id=user_id).first()


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


def responses_for_event(session, event_id):
    return session.query(Response).filter_by(event_id=event_id).all()


def _get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count
