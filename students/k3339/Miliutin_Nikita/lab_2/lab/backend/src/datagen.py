import asyncio
import random
from datetime import datetime, timedelta

# важно импортировать все модели заранее, чтобы не было ошибок при маппинге
from src.models import airlane, base, flight, reservation, review, seat, ticket, user
from src.database import AsyncSessionLocal
from src.models.flight import Flight, FlightTypeEnum, FlightStatusEnum

DESTINATIONS = [
    "Moscow",
    "Saint Petersburg",
    "Novosibirsk",
    "Kazan",
    "Sochi",
    "Vladivostok",
    "Yekaterinburg",
    "Rostov-on-Don",
    "Samara",
]


async def create_flights():
    statuses = list(FlightStatusEnum)
    async with AsyncSessionLocal() as session:
        for i in range(1, 51):
            dep = datetime.utcnow() + timedelta(hours=i)
            arr = dep + timedelta(hours=2)

            flight_type = FlightTypeEnum.DEPARTURE if i % 2 == 0 else FlightTypeEnum.ARRIVAL
            destination = "Kaliningrad" if flight_type == FlightTypeEnum.ARRIVAL else random.choice(DESTINATIONS)

            f = Flight(
                flight_number=f"FL{i:03}",
                destination=destination,
                departure_time=dep,
                arrival_time=arr,
                gate_number=f"G{(i % 10) + 1}",
                flight_type=flight_type,
                flight_status=random.choice(statuses),
                airline_id=random.randint(1, 3),
            )
            session.add(f)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_flights())
