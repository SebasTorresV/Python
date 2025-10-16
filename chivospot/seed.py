from __future__ import annotations

from datetime import datetime, timedelta, time, timezone

from app import create_app
from app.extensions import db
from app.models import Event, EventStatus, Organizer


def _combine(reference: datetime, day_offset: int, hour: int, minute: int = 0) -> datetime:
    base_date = (reference + timedelta(days=day_offset)).date()
    return datetime.combine(base_date, time(hour=hour, minute=minute))


def seed() -> None:
    """Seed the database with example organizers and events."""
    app = create_app()
    with app.app_context():
        if Event.query.count() > 0:
            print("Database already contains events. Skipping seed.")
            return

        reference = datetime.now(timezone.utc).replace(tzinfo=None)

        organizer_a = Organizer(
            name="Chivo Live Productions",
            email="contacto@chivolive.test",
            phone="+503 5555 1111",
            website="https://chivolive.test",
        )
        organizer_b = Organizer(
            name="Weekend Makers",
            email="hola@weekendmakers.test",
            phone="+503 5555 2222",
            website="https://weekendmakers.test",
        )

        weekend_offset = (5 - reference.weekday()) % 7

        events = [
            Event(
                title="Concierto Indie en el Centro",
                category="Música",
                price="Gratis",
                starts_at=_combine(reference, 1, 19),
                ends_at=_combine(reference, 1, 22),
                venue="Foro Central",
                address="Calle Principal 123",
                city="San Salvador",
                lat=13.6929,
                lon=-89.2182,
                source_url="https://eventos.test/indie",
                tickets_url="https://tickets.test/indie",
                status=EventStatus.PUBLISHED,
                organizer=organizer_a,
            ),
            Event(
                title="Feria Gastronómica del Fin de Semana",
                category="Gastronomía",
                price="$5",
                starts_at=_combine(reference, weekend_offset, 12),
                ends_at=_combine(reference, weekend_offset, 20),
                venue="Parque Cuscatlán",
                address="Av. Cuscatlán",
                city="San Salvador",
                lat=13.6894,
                lon=-89.2185,
                source_url="https://eventos.test/feria-gastro",
                tickets_url="https://tickets.test/feria-gastro",
                status=EventStatus.PUBLISHED,
                organizer=organizer_b,
            ),
            Event(
                title="Mercado de Arte y Diseño",
                category="Arte",
                price="Gratis",
                starts_at=_combine(reference, 3, 10),
                ends_at=_combine(reference, 3, 16),
                venue="Casa de la Cultura",
                address="6a Avenida Norte 456",
                city="Santa Tecla",
                lat=13.6769,
                lon=-89.2797,
                source_url="https://eventos.test/arte",
                tickets_url="https://tickets.test/arte",
                status=EventStatus.PUBLISHED,
                organizer=organizer_b,
            ),
            Event(
                title="Charla de Startups y Tecnología",
                category="Tecnología",
                price="$12",
                starts_at=_combine(reference, 7, 18),
                ends_at=_combine(reference, 7, 21),
                venue="Cowork Chivo Hub",
                address="Boulevard de los Héroes 789",
                city="San Salvador",
                lat=13.7045,
                lon=-89.2137,
                source_url="https://eventos.test/startups",
                tickets_url="https://tickets.test/startups",
                status=EventStatus.PUBLISHED,
                organizer=organizer_a,
            ),
        ]

        db.session.add_all([organizer_a, organizer_b, *events])
        db.session.commit()
        print(f"Seeded {len(events)} events.")


if __name__ == "__main__":
    seed()
