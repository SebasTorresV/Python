from __future__ import annotations

from datetime import timedelta

from sqlalchemy import func

from .extensions import db


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamp columns."""

    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )


class Organizer(TimestampMixin, db.Model):
    __tablename__ = "organizers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    website = db.Column(db.String(255))

    events = db.relationship(
        "Event",
        back_populates="organizer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover - representation only
        return f"<Organizer {self.id} {self.name!r}>"


class EventStatus:
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

    ALL = (DRAFT, PUBLISHED, ARCHIVED)


class Event(TimestampMixin, db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.String(50))
    starts_at = db.Column(db.DateTime, nullable=False)
    ends_at = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(200))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    source_url = db.Column(db.String(255))
    tickets_url = db.Column(db.String(255))
    status = db.Column(db.String(20), nullable=False, default=EventStatus.DRAFT)

    organizer_id = db.Column(
        db.Integer,
        db.ForeignKey("organizers.id", ondelete="SET NULL"),
        nullable=True,
    )

    organizer = db.relationship("Organizer", back_populates="events")

    def __repr__(self) -> str:  # pragma: no cover - representation only
        return f"<Event {self.id} {self.title!r} ({self.status})>"

    @property
    def is_published(self) -> bool:
        return self.status == EventStatus.PUBLISHED

    @property
    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at
