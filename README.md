# E-commerce API (Django/DRF) — Student Demo

A student/demo project for building an e-commerce REST API using Django + Django REST Framework.  
Includes demo OTP authentication, JWT tokens, and Swagger/OpenAPI documentation.

---

## Tech Stack
- Python / Django
- Django REST Framework (DRF)
- JWT Authentication (SimpleJWT)
- Swagger/OpenAPI (drf-spectacular)
- SQLite (demo database)

---

## Project Structure
This repository contains the following main apps:
- `accounts` (Demo OTP + JWT + Profile)
- `catalog` (Product catalog)
- `cart` (Shopping cart)
- `orders` (Orders)
- `payments` (Payments)
- `promotions` (Discounts / Promotions)
- `inventory` (Inventory)

---

## Setup & Run

### 1) Create a virtual environment & install dependencies
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt
