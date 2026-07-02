# Lamya's Cozy Knots — E-commerce Platform

A full e-commerce website for a Tunisian handmade bags brand, built with Django and Docker.

## Stack
- Backend: Django 4.2
- Database: PostgreSQL
- Cache/Sessions: Redis
- Web server: Nginx + Gunicorn
- Frontend: Django Templates + Bootstrap 5
- Containerization: Docker + Docker Compose

## Features (completed)
- Dockerized architecture (web, db, redis, nginx)
- Product catalog with categories and variants (color, size, material)
- User authentication (register, login, profile)
- Session-based cart
- Cash on delivery checkout
- Multilingual support (AR/FR/EN)
- Custom color palette and responsive design

## Features (in progress)
- Order tracking
- Wishlist
- Shipping management by wilaya

## Run locally
git clone ...
cd ecommerce
cp .env.example .env
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
