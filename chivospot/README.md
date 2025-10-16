# Chivospot

Chivospot es un MVP de descubrimiento de eventos construido con Flask y SQLite. El
objetivo inicial es listar eventos ordenados por proximidad y fecha, ofreciendo
filtros rápidos y accesos directos para obtener rutas o comprar boletos.

## Características del MVP

- Application factory con Flask y extensiones preconfiguradas (SQLAlchemy, Migrate).
- Modelos `Organizer` y `Event` con campos para catálogo, ubicaciones y timestamps.
- Plantillas HTML para la lista y el detalle de eventos, usando estilos base en `static/`.
- Ordenamiento por distancia cuando el usuario comparte ubicación (`lat`/`lon`).
- Filtros rápidos por fecha (hoy/fin de semana/próximos), categoría y precio.
- Endpoint de salud `/health` y rutas públicas `/` y `/events/<id>` listas para despliegue.
- Script de semillas `seed.py` con datos de ejemplo para pruebas manuales.

## Configuración rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajusta los valores según tu entorno
flask --app app:create_app run
```

Las variables del archivo `.env` controlan la base de datos, el modo debug y la
clave secreta. Por defecto se utilizará `instance/chivospot.sqlite`.

## Migraciones y base de datos

El repositorio incluye la migración inicial (`migrations/versions/*create_events_schema.py`).
Para preparar la base de datos local ejecuta:

```bash
flask --app app:create_app db upgrade
```

Esto creará `instance/chivospot.sqlite` con las tablas `organizers` y `events`.

## Datos de ejemplo

Para cargar eventos de prueba utiliza el script de semillas:

```bash
python seed.py
```

El script crea dos organizadores y cuatro eventos publicados con distintas
categorías, precios y ubicaciones para probar filtros y ordenamientos.

## Desarrollo y próximos pasos

- Añadir formularios para que los organizadores envíen eventos (`/organizer/submit`).
- Publicar endpoints JSON (`/api/events`) para integraciones externas.
- Implementar autenticación y validaciones adicionales antes de abrir autopublicación.
