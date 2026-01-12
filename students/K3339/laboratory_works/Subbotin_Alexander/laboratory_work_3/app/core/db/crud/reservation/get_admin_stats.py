import logging
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models.reservation import Reservation
from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


async def get_admin_stats(db: AsyncSession) -> dict:
    """
    Get statistics for admin panel.
    
    Returns:
        dict with:
        - confirmed_reservations: number of confirmed reservations
        - total_revenue: sum of prices for confirmed reservations
        - total_customers: number of unique customers with confirmed reservations
    """
    logger.info("Fetching admin statistics")
    
    # Count confirmed reservations
    count_stmt = select(func.count()).select_from(Reservation).where(Reservation.status == 'confirmed')
    count_result = await db.execute(count_stmt)
    confirmed_count = count_result.scalar() or 0
    
    # Calculate total revenue (sum of tour prices for confirmed reservations)
    revenue_stmt = (
        select(func.sum(Tour.price))
        .select_from(Reservation)
        .join(Tour, Reservation.tour_id == Tour.id)
        .where(Reservation.status == 'confirmed')
    )
    revenue_result = await db.execute(revenue_stmt)
    total_revenue = revenue_result.scalar() or 0
    
    # Count unique customers with confirmed reservations
    customers_stmt = (
        select(func.count(func.distinct(Reservation.user_id)))
        .where(Reservation.status == 'confirmed')
    )
    customers_result = await db.execute(customers_stmt)
    total_customers = customers_result.scalar() or 0
    
    logger.info(f"Stats: {confirmed_count} reservations, {total_revenue} revenue, {total_customers} customers")
    
    return {
        "confirmed_reservations": confirmed_count,
        "total_revenue": float(total_revenue),
        "total_customers": total_customers
    }
