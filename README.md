<div align="center">

# 🚗 YouCars

**A modern car marketplace — browse listings, post ads, chat with sellers, and more**

[![Vue](https://img.shields.io/badge/Vue-3.x-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org)
[![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)](https://www.djangoproject.com)
[![Ant Design Vue](https://img.shields.io/badge/Ant%20Design-4.x-0170FE?logo=antdesign&logoColor=white)](https://antdv.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[🐛 Bug Report](https://github.com/javohir-tech/youcars/issues)

</div>

---

## ✨ Features

| Module | Description |
|---|---|
|  **Authentication** | Sign up, login, email verification, password reset |
|  **Car Listings** | Browse cars by type (avtomobil, transport, moto), filter by brand/model/color/fuel/country |
|  **Catalog** | Full catalog with advanced search & filter |
|  **Car Upload** | Post a new car ad with images, update or archive existing ones |
|  **Favorites** | Like/dislike cars, view saved listings |
|  **Similar Cars** | Related listings on car detail page |
|  **Blog / News** | Blog posts with detail view and similar articles |
|  **Real-time Chat** | WebSocket-based messaging between users (Django Channels) |
|  **Profile** | User info, avatar, my cars (published / draft / archived) |
|  **i18n** | English 🇬🇧 / O'zbek 🇺🇿 / Русский 🇷🇺 |

---

## 🏗 Architecture

```
youcars/
├── client/                  # Vue 3 + Vite + TypeScript
│   └── src/
│       ├── views/           # Pages (Home, Katalog, CarDetail, Chat, ...)
│       ├── components/      # Shared UI (CarCard, BlogCard, Filter, Navbar, ...)
│       ├── auth/            # Login, Signup, ForgetPassword, Verify
│       ├── profile/         # Profile settings, MyCars, Storage, CarUpload
│       ├── layout/          # mainLayout, profileLayout, myCarsLayout
│       ├── store/           # Pinia stores (useUserStore, ...)
│       ├── composables/     # Reusable logic
│       ├── router/          # Vue Router (auth guards included)
│       ├── i18n/            # vue-i18n (uz / ru / en)
│       └── utils/           # Helpers
│
└── server/                  # Django 5 + Django REST Framework
    ├── users/               # Auth, JWT, email verification
    ├── cars/                # Car listings, brands, models, filters, likes
    ├── blog/                # Blog posts
    └── websoket/            # Django Channels — WebSocket chat
```

---

## 🚀 Getting Started

### Prerequisites

- Python `3.12+`
- Node.js `20+`
- npm or pnpm

---

### Backend (Django)

```bash
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Server runs at `http://localhost:8000`

API docs available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

---

### Frontend (Vue + Vite)

```bash
cd client

# Install dependencies
npm install

# Start dev server
npm run dev
```

App runs at `http://localhost:5173`

---

## 🔌 API Reference

### Auth — `/auth/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/singup/` | Register a new user |
| POST | `/auth/verify/` | Verify confirmation code |
| POST | `/auth/login/` | Login |
| POST | `/auth/logout/` | Logout |
| POST | `/auth/forget/` | Request password reset |
| POST | `/auth/new_password/` | Set new password |
| PATCH | `/auth/user/update/` | Update user info |
| PATCH | `/auth/password/update/` | Change password |
| GET | `/auth/user/` | Get current user |
| POST | `/auth/refresh/` | Refresh JWT token |
| DELETE | `/auth/user/image/delete/<id>/` | Delete avatar |
| POST | `/auth/email/` | Request email change |
| POST | `/auth/email/verify/` | Verify new email |

### Cars — `/cars/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cars/cars/` | List all cars (with filters) |
| POST | `/cars/car/` | Create a car listing |
| GET/PUT/PATCH/DELETE | `/cars/car/<id>/` | Car detail / update / delete |
| POST | `/cars/car/image/` | Upload car image |
| DELETE | `/cars/car/image/<id>/` | Delete car image |
| GET | `/cars/marka/` | Brands by type |
| GET | `/cars/models/` | Models by brand |
| GET | `/cars/colors/` | Colors list |
| GET | `/cars/countries/` | Countries list |
| GET | `/cars/fuel/` | Fuel types |
| GET | `/cars/avtotype/` | Vehicle types |
| GET | `/cars/user/cars/draft/` | My draft listings |
| GET | `/cars/user/cars/published/` | My published listings |
| POST | `/cars/car/like/<id>/` | Like / unlike a car |
| GET | `/cars/cars/meliked/` | My liked cars |
| GET | `/cars/car/similar/<id>/` | Similar cars |
| GET | `/cars/car/banner/` | Banner cars |
| GET | `/cars/filter/` | Search & filter |

### Blog — `/blog/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/blog/blog/` | Create blog post |
| GET | `/blog/blog/all/` | List all posts |
| GET | `/blog/blog/detail/<id>/` | Post detail |
| GET | `/blog/blog/semiler/<id>/` | Similar posts |

### Chat — `/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/conversations/` | List conversations |
| GET | `/api/chat/<id>/history/` | Chat message history |

> Real-time messaging is handled via **WebSocket** at `ws://localhost:8000/ws/chat/<room_id>/`

---

## 🛠 Tech Stack

**Frontend**
- [Vue 3](https://vuejs.org) + [Vite](https://vitejs.dev)
- [Ant Design Vue](https://antdv.com) — UI component library
- [Pinia](https://pinia.vuejs.org) — state management
- [Vue Router 4](https://router.vuejs.org) — routing with auth guards
- [vue-i18n](https://vue-i18n.intlify.dev) — internationalization
- [Swiper](https://swiperjs.com) — image sliders
- [Axios](https://axios-http.com) — HTTP client

**Backend**
- [Django 5](https://www.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Django Channels](https://channels.readthedocs.io) — WebSocket support
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io) — JWT authentication
- [drf-yasg](https://drf-yasg.readthedocs.io) — Swagger / ReDoc API docs
- [django-filters](https://django-filter.readthedocs.io) — query filtering
- SQLite (development) / PostgreSQL (production)

---

## 👨‍💻 Author

**Javohir** — [GitHub](https://github.com/javohir-tech)

---

<div align="center">

⭐ If you like this project, please consider giving it a star!

</div>
