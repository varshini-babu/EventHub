from sqlalchemy import Column, Integer, String, BigInteger, Date, Time, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base


class Event(Base):

    __tablename__ = "event"

    event_id = Column(BigInteger, primary_key=True, index=True)
    event_name = Column(String(255))
    event_description = Column(String(255))
    event_date = Column(Date)
    event_time = Column(Time)
    event_venue = Column(String(255))
    event_ticket_price = Column(Integer)
    event_max_of_tickets = Column(Integer)
    event_photo = Column(LargeBinary)

    bookings = relationship("BookedEvent", back_populates="event")


class BookedEvent(Base):

    __tablename__ = "booked_event"

    booking_id = Column(BigInteger, primary_key=True)
    booking_confirmation_code = Column(String(255))
    booking_no_of_tickets = Column(Integer)
    booking_user_email = Column(String(255))
    booking_user_name = Column(String(255))

    event_id = Column(BigInteger, ForeignKey("event.event_id"))

    event = relationship("Event", back_populates="bookings")


class User(Base):

    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True)
    user_email = Column(String(255))
    user_first_name = Column(String(255))
    user_last_name = Column(String(255))
    user_password = Column(String(255))


class Role(Base):

    __tablename__ = "role"

    role_id = Column(BigInteger, primary_key=True)
    role_name = Column(String(255))


class UserRoles(Base):

    __tablename__ = "user_roles"

    user_id = Column(BigInteger, ForeignKey("user.user_id"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("role.role_id"), primary_key=True)