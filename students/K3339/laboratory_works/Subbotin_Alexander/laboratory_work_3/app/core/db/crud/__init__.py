"""
CRUD operations module.

This module provides all database operations for the Tour Agency API.
All CRUD functions are organized by model type (user, tour, reservation, review).
"""

# User CRUD operations
from app.core.db.crud.user.create_user import create_user
from app.core.db.crud.user.get_user import get_user_by_id, get_user_by_username, get_user_by_email
from app.core.db.crud.user.profile import create_user_profile, get_user_profile, update_user_profile
from app.core.db.crud.user.update_user import update_user, update_user_password

# Tour CRUD operations
from app.core.db.crud.tour.create_tour import create_tour
from app.core.db.crud.tour.get_tour import get_tour_by_id
from app.core.db.crud.tour.get_all_tours import get_all_tours
from app.core.db.crud.tour.update_tour import update_tour
from app.core.db.crud.tour.delete_tour import delete_tour

# Reservation CRUD operations
from app.core.db.crud.reservation.create_reservation import create_reservation
from app.core.db.crud.reservation.get_reservation import get_reservation_by_id
from app.core.db.crud.reservation.get_all_reservations import get_all_reservations
from app.core.db.crud.reservation.get_all_reservations_admin import get_all_reservations_admin
from app.core.db.crud.reservation.get_confirmed_reservation import get_confirmed_reservation
from app.core.db.crud.reservation.get_user_reservation_for_tour import get_user_reservation_for_tour
from app.core.db.crud.reservation.get_admin_stats import get_admin_stats
from app.core.db.crud.reservation.update_reservation import update_reservation
from app.core.db.crud.reservation.delete_reservation import delete_reservation

# Review CRUD operations
from app.core.db.crud.review.create_review import create_review
from app.core.db.crud.review.get_review import get_review_by_id
from app.core.db.crud.review.get_reviews_by_tour import get_reviews_by_tour
from app.core.db.crud.review.get_review_by_user_tour import get_review_by_user_tour
from app.core.db.crud.review.update_review import update_review
from app.core.db.crud.review.delete_review import delete_review

# Alias for backward compatibility
get_tours = get_all_tours
get_reservations_by_user = get_all_reservations

__all__ = [
    # User operations
    "create_user",
    "get_user_by_id",
    "get_user_by_username",
    "get_user_by_email",
    "create_user_profile",
    "get_user_profile",
    "update_user_profile",
    "update_user",
    "update_user_password",
    
    # Tour operations
    "create_tour",
    "get_tour_by_id",
    "get_all_tours",
    "get_tours",  # alias
    "update_tour",
    "delete_tour",
    
    # Reservation operations
    "create_reservation",
    "get_reservation_by_id",
    "get_all_reservations",
    "get_all_reservations_admin",
    "get_reservations_by_user",  # alias
    "get_confirmed_reservation",
    "get_user_reservation_for_tour",
    "get_admin_stats",
    "update_reservation",
    "delete_reservation",
    
    # Review operations
    "create_review",
    "get_review_by_id",
    "get_reviews_by_tour",
    "get_review_by_user_tour",
    "update_review",
    "delete_review",
]
