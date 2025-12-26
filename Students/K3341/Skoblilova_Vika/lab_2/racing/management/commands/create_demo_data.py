"""
Management команда для создания демо-данных.
"""
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from racing.models import Team, DriverProfile, Race, Heat, HeatResult, Registration, Comment


class Command(BaseCommand):
    help = 'Создает демо-данные для приложения racing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание демо-данных...')

        # Создаем команды
        teams_data = [
            {'name': 'Скорость', 'description': 'Профессиональная команда с многолетним опытом'},
            {'name': 'Адреналин', 'description': 'Молодая и амбициозная команда'},
            {'name': 'Турбо', 'description': 'Специализация на высокоскоростных гонках'},
            {'name': 'Нитро', 'description': 'Команда чемпионов России по дрифту'},
            {'name': 'Форсаж', 'description': 'Любители кольцевых гонок'},
            {'name': 'Пит-Стоп', 'description': 'Опытные механики и быстрые гонщики'},
        ]
        
        teams = []
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={'description': team_data['description']}
            )
            teams.append(team)
            if created:
                self.stdout.write(f'  Создана команда: {team.name}')

        # Создаем демо-пользователей
        users_data = [
            {'username': 'pilot1', 'email': 'pilot1@racing.com', 'password': 'demo1234'},
            {'username': 'pilot2', 'email': 'pilot2@racing.com', 'password': 'demo1234'},
            {'username': 'pilot3', 'email': 'pilot3@racing.com', 'password': 'demo1234'},
            {'username': 'pilot4', 'email': 'pilot4@racing.com', 'password': 'demo1234'},
            {'username': 'pilot5', 'email': 'pilot5@racing.com', 'password': 'demo1234'},
            {'username': 'pilot6', 'email': 'pilot6@racing.com', 'password': 'demo1234'},
            {'username': 'pilot7', 'email': 'pilot7@racing.com', 'password': 'demo1234'},
            {'username': 'pilot8', 'email': 'pilot8@racing.com', 'password': 'demo1234'},
            {'username': 'pilot9', 'email': 'pilot9@racing.com', 'password': 'demo1234'},
            {'username': 'pilot10', 'email': 'pilot10@racing.com', 'password': 'demo1234'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': f'Пилот {user_data["username"][-1]}',
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'  Создан пользователь: {user.username}')
            users.append(user)

        # Обновляем профили водителей (заполняем обязательные поля)
        profiles_data = [
            {
                'full_name': 'Иван Петров',
                'car_description': 'BMW M3 E46',
                'bio': 'Опытный гонщик с 10-летним стажем',
                'experience_years': 10,
                'driver_class': 'A',
                'team': teams[0]
            },
            {
                'full_name': 'Алексей Сидоров',
                'car_description': 'Nissan Skyline GTR R34',
                'bio': 'Специалист по дрифту и кольцевым гонкам',
                'experience_years': 7,
                'driver_class': 'B',
                'team': teams[1]
            },
            {
                'full_name': 'Сергей Николаев',
                'car_description': 'Subaru Impreza WRX STI',
                'bio': 'Молодой и перспективный гонщик',
                'experience_years': 3,
                'driver_class': 'C',
                'team': teams[1]
            },
            {
                'full_name': 'Дмитрий Козлов',
                'car_description': 'Toyota Supra MK4',
                'bio': 'Чемпион региональных соревнований',
                'experience_years': 8,
                'driver_class': 'A',
                'team': teams[2]
            },
            {
                'full_name': 'Михаил Волков',
                'car_description': 'Mazda RX-7 FD',
                'bio': 'Любитель роторных двигателей',
                'experience_years': 5,
                'driver_class': 'B',
                'team': teams[3]
            },
            {
                'full_name': 'Андрей Смирнов',
                'car_description': 'Honda Civic Type R',
                'bio': 'Фанат JDM культуры',
                'experience_years': 4,
                'driver_class': 'C',
                'team': teams[3]
            },
            {
                'full_name': 'Владимир Кузнецов',
                'car_description': 'Mitsubishi Lancer Evolution IX',
                'bio': 'Призер чемпионата по ралли-кроссу',
                'experience_years': 9,
                'driver_class': 'A',
                'team': teams[4]
            },
            {
                'full_name': 'Павел Морозов',
                'car_description': 'Nissan 350Z',
                'bio': 'Начинающий дрифтер',
                'experience_years': 2,
                'driver_class': 'C',
                'team': teams[4]
            },
            {
                'full_name': 'Артем Федоров',
                'car_description': 'Ford Mustang GT',
                'bio': 'Любитель американских маслкаров',
                'experience_years': 6,
                'driver_class': 'B',
                'team': teams[5]
            },
            {
                'full_name': 'Максим Соколов',
                'car_description': 'Volkswagen Golf GTI',
                'bio': 'Специалист по хэтчбекам',
                'experience_years': 5,
                'driver_class': 'B',
                'team': teams[5]
            },
        ]
        
        for i, user in enumerate(users):
            profile = user.driver_profile
            # Обязательно заполняем full_name
            for key, value in profiles_data[i].items():
                setattr(profile, key, value)
            profile.save()
            self.stdout.write(f'  Обновлен профиль: {profile.full_name}')

        # Создаем гонки
        races_data = [
            {
                'title': 'Весенний Кубок Скорости',
                'location': 'Москва, автодром Moscow Raceway',
                'date': date.today() + timedelta(days=15),
                'description': 'Открытие гоночного сезона. Кольцевые гонки на 20 кругов.',
                'is_published': True,
            },
            {
                'title': 'Битва Титанов',
                'location': 'Санкт-Петербург, Игора Драйв',
                'date': date.today() + timedelta(days=30),
                'description': 'Главное событие сезона! Сражение лучших пилотов страны.',
                'is_published': True,
            },
            {
                'title': 'Ночная гонка',
                'location': 'Москва, Moscow Raceway',
                'date': date.today() + timedelta(days=45),
                'description': 'Уникальная ночная гонка с подсветкой трассы.',
                'is_published': True,
            },
            {
                'title': 'Летний Драг-рейсинг',
                'location': 'Санкт-Петербург, аэродром Левашово',
                'date': date.today() + timedelta(days=60),
                'description': 'Соревнования по разгону на четверть мили. Участвуют самые мощные машины!',
                'is_published': True,
            },
            {
                'title': 'Кубок Поволжья',
                'location': 'Казань, Kazan Ring',
                'date': date.today() + timedelta(days=75),
                'description': 'Региональный этап чемпионата.',
                'is_published': True,
            },
            {
                'title': 'Дрифт Мастерс',
                'location': 'Нижний Новгород, Автодром',
                'date': date.today() + timedelta(days=90),
                'description': 'Профессиональные соревнования по дрифту.',
                'is_published': True,
            },
            {
                'title': 'Осенний марафон',
                'location': 'Казань, Kazan Ring',
                'date': date.today() + timedelta(days=120),
                'description': 'Гонка на выносливость - 4 часа непрерывных заездов.',
                'is_published': True,
            },
            {
                'title': 'Финал сезона',
                'location': 'Сочи, Сочи Автодром',
                'date': date.today() + timedelta(days=150),
                'description': 'Решающая гонка сезона! Определение чемпиона.',
                'is_published': True,
            },
            {
                'title': 'Зимний дрифт',
                'location': 'Сочи, Сочи Автодром',
                'date': date.today() + timedelta(days=180),
                'description': 'Соревнования по дрифту на зимней трассе.',
                'is_published': False,
            },
            {
                'title': 'Новогодний заезд',
                'location': 'Москва, Moscow Raceway',
                'date': date.today() + timedelta(days=210),
                'description': 'Праздничная гонка в честь Нового Года!',
                'is_published': False,
            },
        ]
        
        races = []
        for race_data in races_data:
            race, created = Race.objects.get_or_create(
                title=race_data['title'],
                defaults=race_data
            )
            races.append(race)
            if created:
                self.stdout.write(f'  Создана гонка: {race.title}')

        # Создаем регистрации СНАЧАЛА (до создания результатов)
        # Каждый пользователь регистрируется на 2-4 гонки
        self.stdout.write('\nСоздание регистраций...')
        for i, user in enumerate(users):
            # Выбираем случайные гонки для регистрации
            races_to_register = random.sample(list(races[:8]), random.randint(2, 4))
            
            for race in races_to_register:
                reg, created = Registration.objects.get_or_create(
                    driver=user.driver_profile,
                    race=race,
                    defaults={
                        'car_number': random.randint(1, 99),
                        'active': True
                    }
                )
                if created:
                    self.stdout.write(f'  Регистрация {user.driver_profile.full_name} на {race.title}')
        
        # Создаем заезды для гонок
        self.stdout.write('\nСоздание заездов и результатов...')
        heat_names = ['Квалификация', 'Полуфинал', 'Финал']
        for idx, race in enumerate(races[:6]):  # Для первых 6 опубликованных гонок
            base_time = timezone.now() + timedelta(days=race.date.toordinal() - date.today().toordinal())
            
            # Получаем список зарегистрированных водителей для этой гонки
            registered_drivers = list(Registration.objects.filter(
                race=race, 
                active=True
            ).values_list('driver', flat=True))
            
            if not registered_drivers:
                self.stdout.write(f'  ⚠ Пропуск {race.title} - нет зарегистрированных участников')
                continue
            
            for i, name in enumerate(heat_names):
                # Первые 2 гонки завершены, остальные - в разных статусах
                if idx < 2:
                    status = 'finished'
                elif idx < 4:
                    status = 'finished' if i < 2 else 'scheduled'
                else:
                    status = 'scheduled'
                
                heat, created = Heat.objects.get_or_create(
                    race=race,
                    name=name,
                    defaults={
                        'start_time': base_time + timedelta(hours=i*2),
                        'laps': 5 if name == 'Квалификация' else (8 if name == 'Полуфинал' else 12),
                        'status': status,
                        'info': f'{name} - дистанция {5 if name == "Квалификация" else (8 if name == "Полуфинал" else 12)} кругов'
                    }
                )
                if created:
                    self.stdout.write(f'  Создан заезд {name} для {race.title}')
                    
                    # Создаем результаты для завершенных заездов
                    # ТОЛЬКО для зарегистрированных водителей!
                    if heat.status == 'finished' and registered_drivers:
                        # Берем 5-7 участников из ЗАРЕГИСТРИРОВАННЫХ
                        participants_count = min(random.randint(5, 7), len(registered_drivers))
                        participant_ids = random.sample(registered_drivers, participants_count)
                        
                        for j, driver_id in enumerate(participant_ids):
                            driver_profile = DriverProfile.objects.get(id=driver_id)
                            base_time_sec = 120.0 + random.uniform(0, 15)  # Базовое время 120-135 сек
                            result, res_created = HeatResult.objects.get_or_create(
                                heat=heat,
                                driver=driver_profile,
                                defaults={
                                    'position': j + 1,
                                    'finish_time_seconds': round(base_time_sec + (j * random.uniform(1.5, 3.5)), 3),
                                    'status': 'finished' if j < participants_count - 1 else random.choice(['finished', 'dnf']),
                                    'notes': 'Отличный результат!' if j == 0 else ('Хорошая попытка' if j < 3 else '')
                                }
                            )
                            if res_created:
                                self.stdout.write(f'    Добавлен результат для {driver_profile.full_name}')

        # Создаем комментарии
        comments_data = [
            {
                'text': 'Отличная организация гонки! Все четко и профессионально. Трасса в отличном состоянии.',
                'kind': 'race',
                'rating': 9,
            },
            {
                'text': 'Хотелось бы обсудить возможность спонсорского сотрудничества. У нас есть интересное предложение.',
                'kind': 'cooperation',
                'rating': 8,
            },
            {
                'text': 'Когда будет следующий этап? Очень хочу попасть на финал сезона!',
                'kind': 'other',
                'rating': 7,
            },
            {
                'text': 'Невероятная атмосфера! Трибуны полные, болельщики активные. Спасибо организаторам!',
                'kind': 'race',
                'rating': 10,
            },
            {
                'text': 'Было бы здорово добавить больше категорий для начинающих гонщиков.',
                'kind': 'race',
                'rating': 8,
            },
            {
                'text': 'Интересует размещение рекламы на трассе. С кем можно связаться?',
                'kind': 'cooperation',
                'rating': 7,
            },
            {
                'text': 'Отличная трасса, но нужно улучшить пит-лейн. Слишком узко.',
                'kind': 'race',
                'rating': 7,
            },
            {
                'text': 'Первый раз участвую в таких гонках. Всё понравилось, приеду еще!',
                'kind': 'other',
                'rating': 9,
            },
            {
                'text': 'Судейство на высшем уровне. Все справедливо и прозрачно.',
                'kind': 'race',
                'rating': 10,
            },
            {
                'text': 'Можно ли зарегистрировать команду на будущий сезон? Какие условия?',
                'kind': 'cooperation',
                'rating': 8,
            },
            {
                'text': 'Отличная погода, отличная гонка! Жду не дождусь следующего этапа.',
                'kind': 'other',
                'rating': 9,
            },
            {
                'text': 'Хорошо бы добавить трансляцию в интернете. Не все могут приехать лично.',
                'kind': 'other',
                'rating': 6,
            },
        ]
        
        for i, comment_data in enumerate(comments_data):
            # Распределяем комментарии по разным гонкам
            race = races[i % min(6, len(races))]
            author = users[i % len(users)]
            
            comment, created = Comment.objects.get_or_create(
                race=race,
                author=author,
                heat_date=race.date,
                defaults=comment_data
            )
            if created:
                self.stdout.write(f'  Создан комментарий от {author.username}')

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('ДЕМО-ДАННЫЕ УСПЕШНО СОЗДАНЫ!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write('\n📊 СТАТИСТИКА:')
        self.stdout.write(f'  👥 Команд: {len(teams)}')
        self.stdout.write(f'  🏃 Пользователей: {len(users)}')
        self.stdout.write(f'  🏁 Гонок: {len(races)} ({sum(1 for r in races if r.is_published)} опубликовано)')
        self.stdout.write(f'  🏎️  Заездов: {Heat.objects.count()}')
        self.stdout.write(f'  📝 Регистраций: {Registration.objects.count()}')
        self.stdout.write(f'  🏆 Результатов: {HeatResult.objects.count()}')
        self.stdout.write(f'  💬 Комментариев: {Comment.objects.count()}')
        
        self.stdout.write('\n🔑 ДЕМО-ПОЛЬЗОВАТЕЛИ (все с паролем: demo1234):')
        for user_data in users_data:
            self.stdout.write(f'  • {user_data["username"]} - {user_data["email"]}')

