from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from racing.models import Team, Car, Participant, Race, RaceParticipant, Comment
from datetime import datetime, timedelta
from django.utils import timezone


def parse_time(time_str):
    """Parse time string HH:MM:SS to timedelta"""
    parts = time_str.split(":")
    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


class Command(BaseCommand):
    help = "Load sample data for racing application"

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading sample data...")

        # Create Teams
        teams_data = [
            {
                "name": "Red Bull Racing",
                "country": "Austria",
                "founded_year": 2005,
                "description": "Leading Formula 1 team with multiple championships",
            },
            {
                "name": "Mercedes-AMG Petronas",
                "country": "Germany",
                "founded_year": 2010,
                "description": "Dominant F1 team of the hybrid era",
            },
            {
                "name": "Scuderia Ferrari",
                "country": "Italy",
                "founded_year": 1950,
                "description": "The most successful team in F1 history",
            },
            {
                "name": "McLaren Racing",
                "country": "United Kingdom",
                "founded_year": 1963,
                "description": "Historic British racing team",
            },
        ]
        teams = []
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(**team_data)
            teams.append(team)
            if created:
                self.stdout.write(f"Created team: {team.name}")

        # Create Cars
        cars_data = [
            {
                "model_name": "RB19",
                "manufacturer": "Red Bull",
                "year": 2023,
                "engine_type": "Honda RBPT V6 Turbo",
                "horsepower": 1000,
            },
            {
                "model_name": "W14",
                "manufacturer": "Mercedes",
                "year": 2023,
                "engine_type": "Mercedes V6 Turbo",
                "horsepower": 1000,
            },
            {
                "model_name": "SF-23",
                "manufacturer": "Ferrari",
                "year": 2023,
                "engine_type": "Ferrari V6 Turbo",
                "horsepower": 1000,
            },
            {
                "model_name": "MCL60",
                "manufacturer": "McLaren",
                "year": 2023,
                "engine_type": "Mercedes V6 Turbo",
                "horsepower": 1000,
            },
        ]
        cars = []
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(**car_data)
            cars.append(car)
            if created:
                self.stdout.write(f"Created car: {car}")

        # Create Users and Participants
        participants_data = [
            {
                "username": "max_verstappen",
                "email": "max@example.com",
                "first_name": "Max",
                "last_name": "Verstappen",
                "full_name": "Max Verstappen",
                "country": "Netherlands",
                "dob": "1997-09-30",
                "team": 0,
                "car": 0,
                "experience": "professional",
            },
            {
                "username": "lewis_hamilton",
                "email": "lewis@example.com",
                "first_name": "Lewis",
                "last_name": "Hamilton",
                "full_name": "Lewis Hamilton",
                "country": "United Kingdom",
                "dob": "1985-01-07",
                "team": 1,
                "car": 1,
                "experience": "professional",
            },
            {
                "username": "charles_leclerc",
                "email": "charles@example.com",
                "first_name": "Charles",
                "last_name": "Leclerc",
                "full_name": "Charles Leclerc",
                "country": "Monaco",
                "dob": "1997-10-16",
                "team": 2,
                "car": 2,
                "experience": "professional",
            },
            {
                "username": "lando_norris",
                "email": "lando@example.com",
                "first_name": "Lando",
                "last_name": "Norris",
                "full_name": "Lando Norris",
                "country": "United Kingdom",
                "dob": "1999-11-13",
                "team": 3,
                "car": 3,
                "experience": "advanced",
            },
        ]

        participants = []
        for p_data in participants_data:
            user, created = User.objects.get_or_create(
                username=p_data["username"],
                defaults={
                    "email": p_data["email"],
                    "first_name": p_data["first_name"],
                    "last_name": p_data["last_name"],
                },
            )
            if created:
                user.set_password("password123")
                user.save()

            participant, created = Participant.objects.get_or_create(
                user=user,
                defaults={
                    "full_name": p_data["full_name"],
                    "date_of_birth": p_data["dob"],
                    "country": p_data["country"],
                    "team": teams[p_data["team"]],
                    "car": cars[p_data["car"]],
                    "experience_level": p_data["experience"],
                },
            )
            participants.append(participant)
            if created:
                self.stdout.write(f"Created participant: {participant.full_name}")

        # Create Races
        races_data = [
            {
                "name": "Monaco Grand Prix",
                "location": "Monte Carlo, Monaco",
                "track_length": 3.337,
                "total_laps": 78,
                "date": timezone.now() - timedelta(days=30),
                "status": "completed",
                "description": "The most prestigious race in Formula 1 calendar",
            },
            {
                "name": "British Grand Prix",
                "location": "Silverstone, UK",
                "track_length": 5.891,
                "total_laps": 52,
                "date": timezone.now() - timedelta(days=15),
                "status": "completed",
                "description": "Historic race at the home of British motorsport",
            },
            {
                "name": "Italian Grand Prix",
                "location": "Monza, Italy",
                "track_length": 5.793,
                "total_laps": 53,
                "date": timezone.now() + timedelta(days=7),
                "status": "upcoming",
                "description": "The Temple of Speed - fastest track in F1",
            },
            {
                "name": "Japanese Grand Prix",
                "location": "Suzuka, Japan",
                "track_length": 5.807,
                "total_laps": 53,
                "date": timezone.now() + timedelta(days=21),
                "status": "upcoming",
                "description": "Technical circuit loved by drivers",
            },
        ]

        races = []
        for race_data in races_data:
            race, created = Race.objects.get_or_create(
                name=race_data["name"], defaults=race_data
            )
            races.append(race)
            if created:
                self.stdout.write(f"Created race: {race.name}")

        # Create Race Participants for completed races
        # Monaco GP results
        if races[0].status == "completed":
            results_monaco = [
                {
                    "participant": participants[0],
                    "position": 1,
                    "finish_time": "01:32:15",
                    "best_lap_time": "00:01:12",
                    "points": 25,
                },
                {
                    "participant": participants[1],
                    "position": 2,
                    "finish_time": "01:32:18",
                    "best_lap_time": "00:01:13",
                    "points": 18,
                },
                {
                    "participant": participants[2],
                    "position": 3,
                    "finish_time": "01:32:25",
                    "best_lap_time": "00:01:14",
                    "points": 15,
                },
                {
                    "participant": participants[3],
                    "position": 4,
                    "finish_time": "01:32:30",
                    "best_lap_time": "00:01:14",
                    "points": 12,
                },
            ]

            for result in results_monaco:
                rp, created = RaceParticipant.objects.get_or_create(
                    race=races[0],
                    participant=result["participant"],
                    defaults={
                        "position": result["position"],
                        "finish_time": parse_time(result["finish_time"]),
                        "best_lap_time": parse_time(result["best_lap_time"]),
                        "points": result["points"],
                    },
                )
                if created:
                    self.stdout.write(
                        f'Created race result: {result["participant"].full_name} - P{result["position"]}'
                    )

        # British GP results
        if races[1].status == "completed":
            results_british = [
                {
                    "participant": participants[1],
                    "position": 1,
                    "finish_time": "01:28:45",
                    "best_lap_time": "00:01:27",
                    "points": 25,
                },
                {
                    "participant": participants[0],
                    "position": 2,
                    "finish_time": "01:28:47",
                    "best_lap_time": "00:01:26",
                    "points": 18,
                },
                {
                    "participant": participants[3],
                    "position": 3,
                    "finish_time": "01:29:05",
                    "best_lap_time": "00:01:28",
                    "points": 15,
                },
                {
                    "participant": participants[2],
                    "position": 4,
                    "finish_time": "01:29:12",
                    "best_lap_time": "00:01:29",
                    "points": 12,
                },
            ]

            for result in results_british:
                rp, created = RaceParticipant.objects.get_or_create(
                    race=races[1],
                    participant=result["participant"],
                    defaults={
                        "position": result["position"],
                        "finish_time": parse_time(result["finish_time"]),
                        "best_lap_time": parse_time(result["best_lap_time"]),
                        "points": result["points"],
                    },
                )
                if created:
                    self.stdout.write(
                        f'Created race result: {result["participant"].full_name} - P{result["position"]}'
                    )

        # Register participants for upcoming races
        for race in races[2:]:
            for participant in participants:
                rp, created = RaceParticipant.objects.get_or_create(
                    race=race, participant=participant
                )
                if created:
                    self.stdout.write(
                        f"Registered {participant.full_name} for {race.name}"
                    )

        # Create sample comments
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if _:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write("Created admin user: admin / admin123")

        comments_data = [
            {
                "race": races[0],
                "author": admin_user,
                "type": "track",
                "text": "Amazing race! The track was in perfect condition.",
                "rating": 10,
            },
            {
                "race": races[0],
                "author": User.objects.get(username="lewis_hamilton"),
                "type": "cooperation",
                "text": "Great teamwork and sportsmanship from all drivers.",
                "rating": 9,
            },
            {
                "race": races[1],
                "author": admin_user,
                "type": "track",
                "text": "Silverstone never disappoints! Best track in the calendar.",
                "rating": 10,
            },
        ]

        for comment_data in comments_data:
            comment, created = Comment.objects.get_or_create(
                race=comment_data["race"],
                author=comment_data["author"],
                defaults={
                    "comment_type": comment_data["type"],
                    "text": comment_data["text"],
                    "rating": comment_data["rating"],
                },
            )
            if created:
                self.stdout.write(f"Created comment by {comment.author.username}")

        self.stdout.write(self.style.SUCCESS("Successfully loaded sample data!"))
        self.stdout.write(self.style.SUCCESS("\nLogin credentials:"))
        self.stdout.write(self.style.SUCCESS("Admin: admin / admin123"))
        self.stdout.write(
            self.style.SUCCESS(
                "Users: max_verstappen, lewis_hamilton, charles_leclerc, lando_norris"
            )
        )
        self.stdout.write(self.style.SUCCESS("Password for all users: password123"))
