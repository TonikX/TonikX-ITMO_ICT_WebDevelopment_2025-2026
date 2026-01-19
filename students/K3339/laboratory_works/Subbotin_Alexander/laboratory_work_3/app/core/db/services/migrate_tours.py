import json
import logging
from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db.models.tour import Tour

logger = logging.getLogger(__name__)


async def migrate_tours(db: AsyncSession, json_file_path: str = None) -> int:
    """
    Migrate tours from JSON file to database.
    
    Args:
        db: Async SQLAlchemy session
        json_file_path: Path to JSON file with tours data (optional)
    
    Returns:
        int: Number of tours migrated
        
    Raises:
        ValueError: If JSON file not found or invalid
        
    Example JSON structure:
        [
            {
                "title": "Paris Adventure",
                "agency": "Dream Tours",
                "description": "Amazing trip to Paris",
                "start_date": "2026-03-01T10:00:00",
                "end_date": "2026-03-08T18:00:00",
                "price": 1500.00,
                "city": "Paris",
                "payment_terms": "50% upfront, 50% before departure"
            }
        ]
    """
    # Default path to tours.json in project root
    if json_file_path is None:
        project_root = Path(__file__).parent.parent.parent.parent.parent
        json_file_path = project_root / "tours.json"
    else:
        json_file_path = Path(json_file_path)
    
    # Check if file exists
    if not json_file_path.exists():
        error_msg = f"Tours JSON file not found at: {json_file_path}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Read and parse JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            tours_data = json.load(f)
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format in {json_file_path}: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Error reading file {json_file_path}: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if not isinstance(tours_data, list):
        raise ValueError("JSON file must contain an array of tours")
    
    migrated_count = 0
    
    # Migrate each tour
    for tour_data in tours_data:
        try:
            # Convert date strings to datetime objects if needed
            if isinstance(tour_data.get('start_date'), str):
                tour_data['start_date'] = datetime.fromisoformat(tour_data['start_date'])
            if isinstance(tour_data.get('end_date'), str):
                tour_data['end_date'] = datetime.fromisoformat(tour_data['end_date'])
            
            # Check if tour already exists (by title and agency)
            stmt = select(Tour).where(
                Tour.title == tour_data['title'],
                Tour.agency == tour_data['agency']
            )
            result = await db.execute(stmt)
            existing_tour = result.scalar_one_or_none()
            
            if existing_tour:
                logger.info(f"Tour '{tour_data['title']}' from '{tour_data['agency']}' already exists, skipping...")
                continue
            
            # Create new tour
            tour = Tour(**tour_data)
            db.add(tour)
            migrated_count += 1
            logger.info(f"Migrating tour: {tour_data['title']}")
            
        except KeyError as e:
            logger.error(f"Missing required field in tour data: {e}")
            continue
        except Exception as e:
            logger.error(f"Error migrating tour '{tour_data.get('title', 'Unknown')}': {str(e)}")
            continue
    
    # Commit all changes
    await db.commit()
    logger.info(f"Successfully migrated {migrated_count} tours")
    
    return migrated_count
