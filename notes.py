# ============================================
# REQUEST - RESPONSE CYCLE IN DJANGO
# ============================================

# GET /api/courses/ request flow:

# Browser
#    ↓
# URL Router (urls.py)
#    ↓
# View (views.py)
#    ↓
# Model (models.py) - interacts with database
#    ↓
# Database Query
#    ↓
# Data Returned
#    ↓
# View prepares response
#    ↓
# HttpResponse / JSONResponse
#    ↓
# Browser


# ============================================
# MIDDLEWARE
# ============================================

# Middleware sits between the request and response.
# Every request passes through middleware before reaching views.
# Every response also passes through middleware before returning to the client.

# Example built-in middleware:

# 1. SecurityMiddleware
# Adds security headers and protects against common attacks.

# 2. SessionMiddleware
# Enables session support and manages user session data.


# ============================================
# WSGI vs ASGI
# ============================================

# WSGI (Web Server Gateway Interface)
# - Supports synchronous applications.
# - Traditional Python web standard.
# - Default interface used by Django.

# ASGI (Asynchronous Server Gateway Interface)
# - Supports asynchronous requests.
# - Suitable for WebSockets, real-time chat, and long-lived connections.

# Django uses WSGI by default.
# Switch to ASGI when building asynchronous applications or real-time services.


# ============================================
# MVC and MVT
# ============================================

# MVC:
# Model      -> Data layer
# View       -> User Interface
# Controller -> Business Logic

# Django uses MVT:

# Model    -> Model
# View     -> Controller (handles business logic)
# Template -> View (presentation layer)