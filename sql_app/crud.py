from sqlalchemy.orm import Session
from . import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = models.User(username=user.username)
    # gitのようなイメージ
    db.add(db_user)
    db.commit()
    # session情報などの変更の反映
    db.refresh(db_user)
    return db_user


def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    # gitのようなイメージ
    db.add(db_room)
    db.commit()
    # session情報などの変更の反映
    db.refresh(db_room)
    return db_room


def create_booking(db: Session, booking: schemas.Booking):
    db_booking = models.Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime)
    # gitのようなイメージ
    db.add(db_booking)
    db.commit()
    # session情報などの変更の反映
    db.refresh(db_booking)
    return db_booking
