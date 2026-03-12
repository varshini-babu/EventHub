from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import BookedEvent
from schemas import BookingCreate
import random

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# Generate confirmation code
def generate_confirmation_code():
    return str(random.randint(1000000000, 9999999999))


# Book event
@router.post("/event/{event_id}/booking")
def book_event(event_id: int, booking: BookingCreate, db: Session = Depends(get_db)):

    confirmation_code = generate_confirmation_code()

    new_booking = BookedEvent(
        booking_confirmation_code=confirmation_code,
        booking_no_of_tickets=booking.booking_no_of_tickets,
        booking_user_email=booking.booking_user_email,
        booking_user_name=booking.booking_user_name,
        event_id=event_id
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "message": "Booking successful",
        "confirmation_code": confirmation_code
    }


# Get all bookings
@router.get("/all-bookings")
def get_all_bookings(db: Session = Depends(get_db)):

    bookings = db.query(BookedEvent).all()

    return bookings


# Get booking by confirmation code
@router.get("/confirmation/{confirmationCode}")
def get_booking_by_confirmation_code(confirmationCode: str, db: Session = Depends(get_db)):

    booking = db.query(BookedEvent).filter(
        BookedEvent.booking_confirmation_code == confirmationCode
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


# Cancel booking
@router.delete("/booking/{bookingId}/delete")
def cancel_booking(bookingId: int, db: Session = Depends(get_db)):

    booking = db.query(BookedEvent).filter(
        BookedEvent.booking_id == bookingId
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled successfully"}


# Get bookings by user email
@router.get("/user/{userId}/bookings")
def get_bookings_by_user(userId: int, db: Session = Depends(get_db)):

    bookings = db.query(BookedEvent).all()

    return bookings