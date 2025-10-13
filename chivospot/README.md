# Chivospot

Chivospot es un MVP de descubrimiento de eventos construido con Flask y SQLite. El
objetivo inicial es listar eventos ordenados por proximidad y fecha, ofreciendo
filtros rápidos y accesos directos para obtener rutas o comprar boletos.

## Características del MVP

- API REST sencilla con Flask y arquitectura basada en application factory.
- Base de datos SQLite gestionada con Flask-SQLAlchemy y Flask-Migrate.
- Modelos `Organizer` y `Event` listos para soportar el catálogo de eventos.
- Endpoints iniciales `/health` y `/` como placeholders hasta crear las vistas HTML.
- Estructura preparada para ampliar con blueprints, servicios y plantillas.

## Configuración rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app:create_app run
```

Para entornos de producción, define tus variables en un archivo `.env` (usa
`.env.example` como referencia) o mediante variables de entorno.

## Migraciones

Inicializa y ejecuta migraciones con:

```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

La base de datos SQLite se creará dentro del directorio `instance/`.
