from pydantic import BaseModel


class UserRegister(BaseModel):
    user_first_name: str
    user_last_name: str
    user_email: str
    user_password: str


class UserLogin(BaseModel):
    user_email: str
    user_password: str


class BookingCreate(BaseModel):
    booking_user_name: str
    booking_user_email: str
    booking_no_of_tickets: int