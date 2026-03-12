from fastapi import FastAPI
from routers import events, bookings, users, auth
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(users.router)
app.include_router(auth.router)


