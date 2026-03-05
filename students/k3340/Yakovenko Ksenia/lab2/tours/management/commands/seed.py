from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from tours.models import Country, Agency, Tour, Review
from bookings.models import Booking

class Command(BaseCommand):
    help = "Seed the database with demo data (countries, agencies, tours, reviews, bookings)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo data (tours, bookings, reviews) before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options.get("reset", False)

        if reset:
            self.stdout.write(self.style.WARNING("Resetting demo data..."))
            Booking.objects.all().delete()
            Review.objects.all().delete()
            Tour.objects.all().delete()
            # Keep reference data optional:
            Agency.objects.all().delete()
            Country.objects.all().delete()

        # Reference data
        countries = [
            "Finland",
            "Sweden",
            "Norway",
            "Iceland",
            "Italy",
            "Spain",
            "Japan",
            "Georgia",
            "Portugal",
            "Czech Republic",
        ]
        agencies = [
            "NorthWind Travel",
            "CityBreak Lab",
            "EcoRoute Tours",
        ]

        country_objs = {}
        for name in countries:
            obj, _ = Country.objects.get_or_create(name=name)
            country_objs[name] = obj

        agency_objs = {}
        for name in agencies:
            obj, _ = Agency.objects.get_or_create(name=name)
            agency_objs[name] = obj

        tours_data = [
            dict(
                title="Helsinki + Porvoo: Nordic Weekend",
                agency="CityBreak Lab",
                country="Finland",
                start_date="2026-03-20",
                end_date="2026-03-23",
                price="420.00",
                description="A relaxed city break in Helsinki with seaside walks, saunas, design districts, and a day trip to Porvoo.",
                payment_terms="30% deposit required. Remaining balance due 7 days before departure. Full refund if canceled 14+ days before start, 50% refund if canceled 7-13 days before.",
            ),
            dict(
                title="Lapland: Northern Lights and Husky Safari",
                agency="NorthWind Travel",
                country="Finland",
                start_date="2026-11-12",
                end_date="2026-11-17",
                price="1090.00",
                description="Experience Arctic winter, chase the Northern Lights, and enjoy husky sledding and cozy evenings in a cabin.",
                payment_terms="40% deposit required. Remaining balance due 10 days before departure. Installment option available.",
            ),
            dict(
                title="Stockholm: Islands, Museums, Coffee",
                agency="CityBreak Lab",
                country="Sweden",
                start_date="2026-04-10",
                end_date="2026-04-13",
                price="460.00",
                description="Explore Gamla Stan, museums, waterfront promenades, and take a ferry to one of Stockholm’s islands.",
                payment_terms="20% deposit required. Remaining balance due 5 days before departure. Free cancellation 10+ days before.",
            ),
            dict(
                title="Norwegian Fjords Road Trip",
                agency="NorthWind Travel",
                country="Norway",
                start_date="2026-06-05",
                end_date="2026-06-12",
                price="1480.00",
                description="Travel along breathtaking fjords, visit waterfalls, small villages, and enjoy moderate hiking routes.",
                payment_terms="30% deposit required. Remaining balance due 14 days before departure.",
            ),
            dict(
                title="Iceland Ring Road Adventure",
                agency="NorthWind Travel",
                country="Iceland",
                start_date="2026-08-18",
                end_date="2026-08-26",
                price="2190.00",
                description="Ring road trip including waterfalls, glaciers, black sand beaches, and hot springs.",
                payment_terms="50% deposit required. Remaining balance due 21 days before departure.",
            ),
            dict(
                title="Rome and Florence Classic Tour",
                agency="CityBreak Lab",
                country="Italy",
                start_date="2026-05-02",
                end_date="2026-05-08",
                price="980.00",
                description="Discover ancient Rome and Renaissance Florence with guided highlights and free exploration time.",
                payment_terms="25% deposit required. Remaining balance due 10 days before departure.",
            ),
            dict(
                title="Barcelona: Architecture and Sea",
                agency="CityBreak Lab",
                country="Spain",
                start_date="2026-07-10",
                end_date="2026-07-15",
                price="890.00",
                description="Explore Gaudí’s masterpieces, historic streets, beaches, and vibrant Barcelona atmosphere.",
                payment_terms="30% deposit required. Remaining balance due 10 days before departure.",
            ),
            dict(
                title="Tokyo: Modern City Experience",
                agency="EcoRoute Tours",
                country="Japan",
                start_date="2026-10-03",
                end_date="2026-10-11",
                price="2450.00",
                description="Explore Tokyo neighborhoods, parks, markets, and take a day trip outside the city.",
                payment_terms="40% deposit required. Remaining balance due 20 days before departure.",
            ),
            dict(
                title="Kyoto Autumn Cultural Tour",
                agency="EcoRoute Tours",
                country="Japan",
                start_date="2026-11-05",
                end_date="2026-11-10",
                price="1650.00",
                description="Visit temples, gardens, tea houses, and experience traditional culture in Kyoto during autumn.",
                payment_terms="35% deposit required. Remaining balance due 14 days before departure.",
            ),
            dict(
                title="Tbilisi and Kakheti Wine Tour",
                agency="EcoRoute Tours",
                country="Georgia",
                start_date="2026-04-29",
                end_date="2026-05-04",
                price="640.00",
                description="Explore Tbilisi and enjoy wine tasting in the Kakheti region.",
                payment_terms="20% deposit required. Remaining balance due 7 days before departure.",
            ),
            dict(
                title="Lisbon and Sintra Explorer",
                agency="CityBreak Lab",
                country="Portugal",
                start_date="2026-09-12",
                end_date="2026-09-17",
                price="920.00",
                description="Explore Lisbon’s old districts, ocean views, and take a day trip to Sintra.",
                payment_terms="30% deposit required. Remaining balance due 10 days before departure.",
            ),
            dict(
                title="Prague City Discovery",
                agency="EcoRoute Tours",
                country="Czech Republic",
                start_date="2026-06-20",
                end_date="2026-06-25",
                price="720.00",
                description="Walk through historic Prague, bridges, museums, and charming streets.",
                payment_terms="25% deposit required. Remaining balance due 7 days before departure.",
            ),
        ]

        created_tours = []
        for t in tours_data:
            tour, created = Tour.objects.get_or_create(
                title=t["title"],
                defaults=dict(
                    agency=agency_objs[t["agency"]],
                    country=country_objs[t["country"]],
                    description=t["description"],
                    start_date=t["start_date"],
                    end_date=t["end_date"],
                    payment_terms=t["payment_terms"],
                    price=t["price"],
                ),
            )
            # If it existed, ensure links and fields are up to date (safe for re-run)
            changed = False
            if tour.agency_id != agency_objs[t["agency"]].id:
                tour.agency = agency_objs[t["agency"]]; changed = True
            if tour.country_id != country_objs[t["country"]].id:
                tour.country = country_objs[t["country"]]; changed = True
            for f in ["description", "start_date", "end_date", "payment_terms", "price"]:
                if str(getattr(tour, f)) != str(t[f]):
                    setattr(tour, f, t[f]); changed = True
            if changed:
                tour.save()
            created_tours.append(tour)

        User = get_user_model()
        demo_user, _ = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        if not demo_user.has_usable_password():
            demo_user.set_password("demo12345")
            demo_user.save()

        demo2_user, _ = User.objects.get_or_create(username="demo2", defaults={"email": "demo2@example.com"})
        if not demo2_user.has_usable_password():
            demo2_user.set_password("demo12345")
            demo2_user.save()

        # Reviews (attach to first few tours)
        reviews_data = [
            ("Helsinki + Porvoo: Nordic Weekend", 9, "Very relaxing trip. Porvoo is beautiful and peaceful. Would recommend."),
            ("Norwegian Fjords Road Trip", 10, "Amazing views and great organization. One of the best trips I've ever had."),
            ("Barcelona: Architecture and Sea", 8, "Great experience overall. Barcelona is vibrant, but summer can be hot."),
            ("Tokyo: Modern City Experience", 9, "Tokyo is incredible. The itinerary was well balanced and enjoyable."),
            ("Tbilisi and Kakheti Wine Tour", 9, "Wonderful food and atmosphere. Kakheti day was a highlight."),
        ]

        for title, rating, text in reviews_data:
            tour = Tour.objects.get(title=title)
            Review.objects.get_or_create(
                tour=tour,
                author=demo_user,
                text=text,
                rating=rating,
                defaults=dict(tour_start_date=tour.start_date, tour_end_date=tour.end_date),
            )

        # Bookings (some confirmed to populate sales stats)
        for i, tour in enumerate(created_tours):
            b1, _ = Booking.objects.get_or_create(tour=tour, user=demo_user)
            b2, _ = Booking.objects.get_or_create(tour=tour, user=demo2_user)
            # Confirm every other tour for demo_user, and every third for demo2
            if i % 2 == 0 and not b1.is_confirmed:
                b1.is_confirmed = True
                b1.save()
            if i % 3 == 0 and not b2.is_confirmed:
                b2.is_confirmed = True
                b2.save()

        self.stdout.write(self.style.SUCCESS("Seed completed."))
        self.stdout.write("Demo users:")
        self.stdout.write(" - demo / demo12345")
        self.stdout.write(" - demo2 / demo12345")
        self.stdout.write("Open /admin/ and confirm bookings manually if you want.")
