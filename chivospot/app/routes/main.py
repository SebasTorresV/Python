from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from typing import Optional
from urllib.parse import quote_plus

from flask import Blueprint, abort, render_template, request
from sqlalchemy import or_

from ..extensions import db
from ..models import Event, EventStatus
from ..services.geo import haversine_distance
from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.get("/health")
def health():
    """Return a simple health check payload."""
    return {"status": "ok"}


def _get_weekend_bounds(reference: datetime) -> tuple[datetime, datetime]:
    """Return datetime bounds for the upcoming weekend (Saturday/Sunday)."""
    saturday_offset = (5 - reference.weekday()) % 7
    saturday = reference + timedelta(days=saturday_offset)
    saturday_start = datetime.combine(saturday.date(), time.min)
    sunday_end = datetime.combine((saturday + timedelta(days=1)).date(), time.max)
    return saturday_start, sunday_end


def _build_map_link(event: Event) -> Optional[str]:
    """Return a Google Maps URL for the given event."""
    if event.lat is not None and event.lon is not None:
        return f"https://www.google.com/maps/dir/?api=1&destination={event.lat},{event.lon}"

    parts = [event.venue, event.address, event.city]
    query = ", ".join(part for part in parts if part)
    if query:
        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"
    return None


def _apply_price_filter(query, price_filter: str):
    if price_filter == "free":
        query = query.filter(
            or_(
                Event.price.is_(None),
                Event.price == "",
                Event.price == "0",
                Event.price.ilike("%free%"),
                Event.price.ilike("%gratis%"),
            )
        )
    elif price_filter == "paid":
        query = (
            query.filter(Event.price.is_not(None))
            .filter(Event.price != "")
            .filter(Event.price != "0")
            .filter(~Event.price.ilike("%free%"))
            .filter(~Event.price.ilike("%gratis%"))
        )
    return query


@main_bp.get("/")
def event_list():
    """Render the event list with optional filters and ordering by distance/date."""
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    when_filter = request.args.get("when", "upcoming")
    category_filter = request.args.get("category", "").strip()
    price_filter = request.args.get("price", "").strip()

    query = Event.query.filter(Event.status == EventStatus.PUBLISHED)

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if when_filter == "today":
        start = datetime.combine(now.date(), time.min)
        end = datetime.combine(now.date(), time.max)
        query = query.filter(Event.starts_at >= start, Event.starts_at <= end)
    elif when_filter == "weekend":
        start, end = _get_weekend_bounds(now)
        query = query.filter(Event.starts_at >= start, Event.starts_at <= end)
    else:  # upcoming
        query = query.filter(Event.starts_at >= now)
        when_filter = "upcoming"

    if category_filter:
        query = query.filter(Event.category == category_filter)

    if price_filter:
        query = _apply_price_filter(query, price_filter)

    events = query.order_by(Event.starts_at.asc()).all()

    if lat is not None and lon is not None:
        for event in events:
            if event.lat is not None and event.lon is not None:
                event.distance_km = haversine_distance(lat, lon, event.lat, event.lon)
            else:
                event.distance_km = None
        events.sort(
            key=lambda e: (
                e.distance_km is None,
                e.distance_km if e.distance_km is not None else float("inf"),
                e.starts_at,
            )
        )
    else:
        for event in events:
            event.distance_km = None

    categories = [
        row[0]
        for row in db.session.query(Event.category)
        .filter(
            Event.status == EventStatus.PUBLISHED,
            Event.category.is_not(None),
            Event.category != "",
        )
        .distinct()
        .order_by(Event.category.asc())
    ]

    when_options = [
        ("upcoming", "Próximos"),
        ("today", "Hoy"),
        ("weekend", "Fin de semana"),
    ]

    return render_template(
        "events/list.html",
        events=events,
        when_options=when_options,
        categories=categories,
        filters={
            "when": when_filter,
            "category": category_filter,
            "price": price_filter,
        },
        user_location={"lat": lat, "lon": lon},
    )


@main_bp.get("/events/<int:event_id>")
def event_detail(event_id: int):
    """Render the detail page for a published event."""
    event = (
        Event.query.filter(Event.id == event_id, Event.status == EventStatus.PUBLISHED)
        .first()
    )
    if event is None:
        abort(404)

    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    distance_km: Optional[float] = None
    if lat is not None and lon is not None and event.lat is not None and event.lon is not None:
        distance_km = haversine_distance(lat, lon, event.lat, event.lon)

    return render_template(
        "events/detail.html",
        event=event,
        map_url=_build_map_link(event),
        distance_km=distance_km,
    return jsonify({"status": "ok"})


@main_bp.get("/")
def index() -> str:
    """Temporary landing page placeholder until templates arrive."""
    return (
        "Bienvenido a Chivospot. Pronto podrás descubrir eventos cercanos desde "
        "esta página."
    )
