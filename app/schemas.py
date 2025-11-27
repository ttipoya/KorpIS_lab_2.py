from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, validator

class ClubBase(BaseModel):
    name: str = Field(..., max_length=200)
    address: Optional[str] = Field(None, max_length=300)
    city: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=30)

class ClubCreate(ClubBase):
    pass

class ClubRead(ClubBase):
    club_id: int
    class Config:
        orm_mode = True

class ArenaCreate(BaseModel):
    club_id: int
    name: str = Field(..., max_length=200)
    capacity: Optional[int]
    address: Optional[str]

    @validator('capacity')
    def capacity_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('capacity must be non-negative')
        return v

class ArenaRead(ArenaCreate):
    arena_id: int
    class Config:
        orm_mode = True

class RoomCreate(BaseModel):
    arena_id: int
    name: str = Field(..., max_length=100)
    room_type: Optional[str] = Field(None, max_length=50)
    max_players: Optional[int] = 10

    @validator('max_players')
    def max_players_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('max_players must be positive')
        return v

class RoomRead(RoomCreate):
    room_id: int
    class Config:
        orm_mode = True

class PCSpecCreate(BaseModel):
    cpu: Optional[str]
    gpu: Optional[str]
    ram_gb: Optional[int]
    storage_gb: Optional[int]

class PCSpecRead(PCSpecCreate):
    pc_spec_id: int
    class Config:
        orm_mode = True

class StationCreate(BaseModel):
    room_id: int
    label: str = Field(..., max_length=50)
    pc_spec_id: Optional[int]
    status: Optional[str] = 'available'

class StationRead(StationCreate):
    station_id: int
    class Config:
        orm_mode = True

class PlayerCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    rating: Optional[int] = 1000

class PlayerRead(PlayerCreate):
    player_id: int
    class Config:
        orm_mode = True

class MembershipCreate(BaseModel):
    player_id: int
    club_id: int
    start_date: date
    end_date: Optional[date]
    membership_type: Optional[str]

    @validator('end_date')
    def end_must_be_after_start(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class MembershipRead(MembershipCreate):
    membership_id: int
    class Config:
        orm_mode = True

class GameSessionCreate(BaseModel):
    room_id: int
    started_at: datetime
    ended_at: Optional[datetime]
    game_title: Optional[str]
    host_player_id: Optional[int]

    @validator('ended_at')
    def ended_after_started(cls, v, values):
        if v and 'started_at' in values and v < values['started_at']:
            raise ValueError('ended_at must be after started_at')
        return v

class GameSessionRead(GameSessionCreate):
    session_id: int
    class Config:
        orm_mode = True

class TournamentCreate(BaseModel):
    club_id: int
    name: str
    start_date: Optional[date]
    end_date: Optional[date]
    prize_pool: Optional[float]

    @validator('prize_pool')
    def prize_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('prize_pool must be non-negative')
        return v

class TournamentRead(TournamentCreate):
    tournament_id: int
    class Config:
        orm_mode = True

class MatchCreate(BaseModel):
    tournament_id: Optional[int]
    session_id: Optional[int]
    round: Optional[str]
    winner_player_id: Optional[int]

class MatchRead(MatchCreate):
    match_id: int
    class Config:
        orm_mode = True

class StaffCreate(BaseModel):
    club_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    hire_date: Optional[date]

class StaffRead(StaffCreate):
    staff_id: int
    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    player_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    status: Optional[str] = 'pending'

    @validator('end_time')
    def end_after_start(cls, v, values):
        if v and 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class BookingRead(BookingCreate):
    booking_id: int
    class Config:
        orm_mode = True

class ConfigKVCreate(BaseModel):
    config_key: str
    config_value: str
    club_id: Optional[int]

class ConfigKVRead(ConfigKVCreate):
    class Config:
        orm_mode = True

class PriceKVCreate(BaseModel):
    price_key: str
    price_value: float
    currency: Optional[str] = 'RUB'
    club_id: Optional[int]

    @validator('price_value')
    def price_positive(cls, v):
        if v < 0:
            raise ValueError('price_value must be non-negative')
        return v

class PriceKVRead(PriceKVCreate):
    class Config:
        orm_mode = True
