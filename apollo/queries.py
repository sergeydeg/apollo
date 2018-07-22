from sqlalchemy.orm import joinedload

from .models import Event, EventChannel, Guild, Response, User


def find_event_channel(db, event_channel_id):
    with db.new() as session:
        return session.query(EventChannel). \
            options(joinedload('events').joinedload('responses')). \
            filter_by(id=event_channel_id). \
            first()


def find_event(db, event_id):
    with db.new() as session:
        return session.query(Event). \
            options(joinedload('event_channel')). \
            options(joinedload('responses')). \
            first()


def find_event_from_message(db, message_id):
    with db.new() as session:
        return session.query(Event).filter_by(message_id=message_id).first()


def find_or_create_response(db, user_id, event_id):
    with db.new() as session:
        response = session.query(Response). \
            filter_by(user_id=user_id, event_id=event_id).first()
        if not response:
            response = Response(user_id=user_id, event_id=event_id)
            session.add(response)
    return response


def find_or_create_user(db, user_id):
    return find_or_create_model(db, User, user_id)


def find_or_create_guild(db, guild_id):
    return find_or_create_model(db, Guild, guild_id)


def find_or_create_model(db, Model, model_id):
    with db.new() as session:
        model = session.query(Model).filter(Model.id == model_id).first()
        if not model:
            model = Model(id=model_id)
            session.add(model)
    return model
