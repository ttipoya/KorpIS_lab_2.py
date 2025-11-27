from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Club(Base):
    __tablename__ = 'Club'
    club_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(300))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(30))

    arenas = relationship('Arena', back_populates='club', cascade='all, delete-orphan')
    memberships = relationship('Membership', back_populates='club')
    tournaments = relationship('Tournament', back_populates='club')
    staff = relationship('Staff', back_populates='club')

class ConfigKV(Base):
    __tablename__ = 'ConfigKV'
    config_key: Mapped[str] = mapped_column(String(100), primary_key=True)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    club_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('Club.club_id'))

class PriceKV(Base):
    __tablename__ = 'PriceKV'
    price_key: Mapped[str] = mapped_column(String(100), primary_key=True)
    price_value: Mapped[float] = mapped_column(DECIMAL(10,2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default='RUB')
    club_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('Club.club_id'))

class Arena(Base):
    __tablename__ = 'Arena'
    arena_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('Club.club_id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    capacity: Mapped[Optional[int]] = mapped_column(Integer)
    address: Mapped[Optional[str]] = mapped_column(String(300))

    club = relationship('Club', back_populates='arenas')
    rooms = relationship('Room', back_populates='arena', cascade='all, delete-orphan')

class Room(Base):
    __tablename__ = 'Room'
    room_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    arena_id: Mapped[int] = mapped_column(Integer, ForeignKey('Arena.arena_id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    room_type: Mapped[Optional[str]] = mapped_column(String(50))
    max_players: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    arena = relationship('Arena', back_populates='rooms')
    stations = relationship('Station', back_populates='room', cascade='all, delete-orphan')
    game_sessions = relationship('GameSession', back_populates='room')
    bookings = relationship('Booking', back_populates='room')

class PCSpec(Base):
    __tablename__ = 'PCSpec'
    pc_spec_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cpu: Mapped[Optional[str]] = mapped_column(String(100))
    gpu: Mapped[Optional[str]] = mapped_column(String(100))
    ram_gb: Mapped[Optional[int]] = mapped_column(Integer)
    storage_gb: Mapped[Optional[int]] = mapped_column(Integer)

    stations = relationship('Station', back_populates='pc_spec')

class Station(Base):
    __tablename__ = 'Station'
    station_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('Room.room_id', ondelete='CASCADE'), nullable=False)
    label: Mapped[str] = mapped_column(String(50), nullable=False)
    pc_spec_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('PCSpec.pc_spec_id'))
    status: Mapped[Optional[str]] = mapped_column(String(30), nullable=False, default='available')

    room = relationship('Room', back_populates='stations')
    pc_spec = relationship('PCSpec', back_populates='stations')

class Player(Base):
    __tablename__ = 'Player'
    player_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(200), unique=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, default=1000)

    memberships = relationship('Membership', back_populates='player', cascade='all, delete-orphan')
    hosted_sessions = relationship('GameSession', back_populates='host_player')
    matches_won = relationship('Match', back_populates='winner_player')
    bookings = relationship('Booking', back_populates='player')

class Membership(Base):
    __tablename__ = 'Membership'
    membership_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey('Player.player_id', ondelete='CASCADE'), nullable=False)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('Club.club_id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[Date]] = mapped_column(Date)
    membership_type: Mapped[Optional[str]] = mapped_column(String(50))

    player = relationship('Player', back_populates='memberships')
    club = relationship('Club', back_populates='memberships')

class GameSession(Base):
    __tablename__ = 'GameSession'
    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('Room.room_id'), nullable=False)
    started_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    ended_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    game_title: Mapped[Optional[str]] = mapped_column(String(200))
    host_player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('Player.player_id'))

    room = relationship('Room', back_populates='game_sessions')
    host_player = relationship('Player', back_populates='hosted_sessions')
    matches = relationship('Match', back_populates='session')

class Tournament(Base):
    __tablename__ = 'Tournament'
    tournament_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('Club.club_id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    start_date: Mapped[Optional[Date]] = mapped_column(Date)
    end_date: Mapped[Optional[Date]] = mapped_column(Date)
    prize_pool: Mapped[Optional[float]] = mapped_column(DECIMAL(12,2), default=0)

    club = relationship('Club', back_populates='tournaments')
    matches = relationship('Match', back_populates='tournament', cascade='all, delete-orphan')

class Match(Base):
    __tablename__ = 'Match'
    match_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tournament_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('Tournament.tournament_id', ondelete='CASCADE'))
    session_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('GameSession.session_id'))
    round: Mapped[Optional[str]] = mapped_column(String(50))
    winner_player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('Player.player_id'))

    tournament = relationship('Tournament', back_populates='matches')
    session = relationship('GameSession', back_populates='matches')
    winner_player = relationship('Player', back_populates='matches_won')

class Staff(Base):
    __tablename__ = 'Staff'
    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    club_id: Mapped[int] = mapped_column(Integer, ForeignKey('Club.club_id'), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    role: Mapped[Optional[str]] = mapped_column(String(100))
    hire_date: Mapped[Optional[Date]] = mapped_column(Date)

    club = relationship('Club', back_populates='staff')

class Booking(Base):
    __tablename__ = 'Booking'
    booking_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey('Player.player_id'), nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey('Room.room_id'), nullable=False)
    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String(30), default='pending')

    player = relationship('Player', back_populates='bookings')
    room = relationship('Room', back_populates='bookings')

class RequestLog(Base):
    __tablename__ = 'RequestLog'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    method: Mapped[str] = mapped_column(String(10))
    path: Mapped[str] = mapped_column(String(500))
    status_code: Mapped[int] = mapped_column(Integer)
    duration_ms: Mapped[int] = mapped_column(Integer)
    client_host: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
