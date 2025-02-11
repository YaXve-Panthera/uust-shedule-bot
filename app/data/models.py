from pydantic import BaseModel
from datetime import date

class Group(BaseModel):
    id: int
    name: str
    course: int
    faculty_id: int

class Faculty(BaseModel):
    id: int
    name: str
    city: str

class WeekSchedule(BaseModel):
    id: int
    date: date
    group_id: int
    week: int
    schedule: str

class User(BaseModel):
    id: int
    date_of_registry: date
    group_id: int
    mailing: bool
    mailing_type: str
    mailing_time: str

