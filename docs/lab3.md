# Лабораторная работа №3. Реализация серверной части на django rest. Документирование API..
***
**Автор:** Машковцева Марина
***
**Цель:** овладеть практическими навыками и умениями реализации web-сервисов
средствами Django.
## 10 Вариант:
Создать программную систему, предназначенную для администратора лечебной
клиники.

Прием пациентов ведут несколько врачей различных специализаций. На каждого
пациента клиники заводится медицинская карта, в которой отражается вся
информация по личным данным больного и истории его заболеваний (диагнозы). При
очередном посещении врача в карте отражается дата и время приема, диагноз, текущее
состояние больного, рекомендации по лечению. Так как прием ведется только на
коммерческой основе, после очередного посещения пациент должен оплатить
медицинские услуги (каждый прием оплачивается отдельно). Расчет стоимости
посещения определяется врачом согласно прейскуранту по клинике.

Для ведения внутренней отчетности необходима следующая информация о врач:
фамилия, имя, отчество, специальность, образование, пол, дата рождения и дата начала
и окончания работы в клинике, данные по трудовому договору. Для каждого врача
составляется график работы с указанием рабочих и выходных дней.

Прием пациентов врачи могут вести в разных кабинетах. Каждый кабинет имеет
определенный режим работы, ответственного и внутренний телефон.

## Реализация проекта:
### 1. Модель базы данных средствами DjangoORM
Сначала была реализована диаграмма, наглядно демонстрирующая все связи будущей БД:
![БД](images/Диаграмма%2010%20вар.png)
Затем она же была реализована в проекте:
```python

class Patient(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    passport_data = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Doctor(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    specialty = models.CharField(max_length=100)
    education = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    work_start_date = models.DateField()
    work_end_date = models.DateField(blank=True, null=True)
    contract_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.last_name} ({self.specialty})"

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    work_date = models.DateField()
    is_working = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'work_date')

    def __str__(self):
        return f"{self.doctor} - {self.work_date} {'work' if self.is_working else 'off'}"

class Room(models.Model):
    room_number = models.CharField(max_length=20)
    work_time_start = models.TimeField()
    work_time_end = models.TimeField()
    responsible_person = models.CharField(max_length=100, blank=True, null=True)
    internal_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number}"

class MedicalRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_record')
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"MR:{self.patient}"

class Visit(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='visits')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='visits')
    visit_datetime = models.DateTimeField()
    diagnosis = models.TextField(blank=True, null=True)
    patient_condition = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Visit {self.id} - {self.record.patient} @ {self.visit_datetime}"

class Payment(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='payment')
    payment_datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - visit {self.visit_id}"
```

### 2. Работа API средствами Django REST Framework
Были созданы ModelSerializer-ы для каждой модели:
```python
from rest_framework import serializers
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = "__all__"

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = "__all__"

class VisitSerializer(serializers.ModelSerializer):
    record = MedicalRecordSerializer(read_only=True)
    record_id = serializers.PrimaryKeyRelatedField(queryset=MedicalRecord.objects.all(), source='record', write_only=True)
    class Meta:
        model = Visit
        fields = ["id","record","record_id","doctor","room","visit_datetime","diagnosis","patient_condition","recommendations","price"]

class PaymentSerializer(serializers.ModelSerializer):
    visit = VisitSerializer(read_only=True)
    visit_id = serializers.PrimaryKeyRelatedField(queryset=Visit.objects.all(), source='visit', write_only=True)
    class Meta:
        model = Payment
        fields = ["id","visit","visit_id","payment_datetime","amount","payment_method"]
```
Здесь мы превращаем модели в JSON и обратно, валидируем данные.

А также прописаны ViewSet-ы для каждой модели:
```python
from rest_framework import viewsets, filters, status
from .models import Patient, Doctor, DoctorSchedule, Room, MedicalRecord, Visit, Payment
from .serializers import PatientSerializer, DoctorSerializer, DoctorScheduleSerializer, RoomSerializer, MedicalRecordSerializer, VisitSerializer, PaymentSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('last_name')
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['last_name','first_name','phone']
    ordering_fields = ['last_name','birth_date']

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related('doctor','record__patient','room').all()
    serializer_class = VisitSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('visit__record__patient').all()
    serializer_class = PaymentSerializer
```
Здесь мы подключаем сериалайзеры и модели, реализуем CRUD (create / read / update / delete).

И в `clinic/urls.py` подключаем все ViewSet'ы через router:
```python
router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('doctors', DoctorViewSet)
```
Здесь создаются все эндпоинты автоматически.
### 3. Подключение регистрации / авторизации по токенам / вывод информации о текущем пользователе средствами Djoser
Подключаем Djoser приложение и JWT в `settings.py`:
```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
]
```

Настройки в разделе REST_FRAMEWORK:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```
Здесь мы говорим использовать JWT токены как метод авторизации.

Настройки DJOSER:
```python
DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
}
```
Здесь включаем регистрацию + повтор ввода пароля.

Далее в файле `urls.py` подключаются маршруты Djoser:
```python
path('auth/', include('djoser.urls')),
path('auth/', include('djoser.urls.jwt')),
```

### 4. Эндпоинты аутентификации и регистрации (Djoser)
#### Важные по заданию:
#### 1. POST /auth/users/
    Создаёт нового пользователя системы.
    Требуется только для того, чтобы иметь возможность войти и получить токен.
#### 2. POST /auth/jwt/create/
    Пользователь вводит логин/пароль, сервер отдаёт:
    access-токен
    refresh-токен
#### 3. GET /auth/users/me/
    Работает только если отправлен Authorization: Bearer <token>.
    Используется для проверки:
    — корректен ли токен
    — кто сейчас авторизован
Djoser автоматически генерирует дополнительные эндпоинты для сброса пароля, проверки токена, обновления токена, активации аккаунта и других функций.

В рамках данного задания они не используются, но присутствуют, так как являются частью стандартного функционала Djoser.

### 5. Эндпоинты API клиники (CRUD)
Каждый ViewSet даёт 5 методов:

- GET /api/'<'model'>'/ — список записей

- POST /api/'<'model'>'/ — создание

- GET /api/'<'model'>'/{id}/ — просмотр одной

- PUT/PATCH /api/'<'model'>'/{id}/ — обновление

- DELETE /api/'<'model'>'/{id}/ — удаление

Все защищены авторизацией, то есть требуют токена.

