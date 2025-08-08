# Inventario Vehicular – H. Ayuntamiento de Hermosillo

Proyecto base en Django 5 + DRF para gestionar el inventario de vehículos.

## Requisitos
- Docker y Docker Compose

## Desarrollo
```bash
docker compose build
docker compose up
```
Aplicar migraciones y datos de ejemplo:
```bash
docker compose run web python manage.py migrate
docker compose run web python manage.py seed_data
```
Acceder a `http://localhost:8000/admin` con usuario `admin` / `admin`.
