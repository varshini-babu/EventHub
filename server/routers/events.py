from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Event
import base64

router = APIRouter(prefix="/events", tags=["Events"])


# Add new event
@router.post("/add/new-event", status_code=201)
async def add_event(
    event_photo: UploadFile = File(...),
    event_name: str = Form(...),
    event_date: str = Form(...),
    event_description: str = Form(...),
    event_time: str = Form(...),
    event_venue: str = Form(...),
    event_ticket_price: int = Form(...),
    event_max_of_tickets: int = Form(...),
    db: Session = Depends(get_db)
):

    photo_bytes = await event_photo.read()

    new_event = Event(
        event_name=event_name,
        event_date=event_date,
        event_description=event_description,
        event_time=event_time,
        event_venue=event_venue,
        event_ticket_price=event_ticket_price,
        event_max_of_tickets=event_max_of_tickets,
        event_photo=photo_bytes
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {"message": "Event created successfully"}


# Get all event names
@router.get("/event/name")
def get_event_names(db: Session = Depends(get_db)):

    events = db.query(Event.event_name).all()

    return [e[0] for e in events]


# Get all events
@router.get("/all-events")
def get_all_events(db: Session = Depends(get_db)):

    events = db.query(Event).all()

    event_list = []

    for event in events:

        photo = None

        if event.event_photo:
            photo = base64.b64encode(event.event_photo).decode("utf-8")

        event_list.append({
            "event_id": event.event_id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "event_date": str(event.event_date),
            "event_time": str(event.event_time),
            "event_venue": event.event_venue,
            "event_ticket_price": event.event_ticket_price,
            "event_max_of_tickets": event.event_max_of_tickets,
            "event_photo": photo
        })

    return event_list


# Get event by ID
@router.get("/event/{eventId}")
def get_event(eventId: int, db: Session = Depends(get_db)):

    event = db.query(Event).filter(Event.event_id == eventId).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    photo = None
    if event.event_photo:
        photo = base64.b64encode(event.event_photo).decode("utf-8")

    return {
        "event_id": event.event_id,
        "event_name": event.event_name,
        "event_description": event.event_description,
        "event_date": str(event.event_date),
        "event_time": str(event.event_time),
        "event_venue": event.event_venue,
        "event_ticket_price": event.event_ticket_price,
        "event_max_of_tickets": event.event_max_of_tickets,
        "event_photo": photo
    }


# Delete event
@router.delete("/delete/event/{eventId}")
def delete_event(eventId: int, db: Session = Depends(get_db)):

    event = db.query(Event).filter(Event.event_id == eventId).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}


# Update event
@router.put("/update/{eventId}")
async def update_event(
    eventId: int,
    event_photo: UploadFile = File(None),
    event_name: str = Form(...),
    event_date: str = Form(...),
    event_description: str = Form(...),
    event_time: str = Form(...),
    event_venue: str = Form(...),
    event_ticket_price: int = Form(...),
    event_max_of_tickets: int = Form(...),
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(Event.event_id == eventId).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.event_name = event_name
    event.event_date = event_date
    event.event_description = event_description
    event.event_time = event_time
    event.event_venue = event_venue
    event.event_ticket_price = event_ticket_price
    event.event_max_of_tickets = event_max_of_tickets

    if event_photo:
        event.event_photo = await event_photo.read()

    db.commit()

    return {"message": "Event updated successfully"}