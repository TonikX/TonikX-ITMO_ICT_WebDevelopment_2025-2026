from django.db import models


# Компания
class Company(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name


# Самолет (борт)
class Aircraft(models.Model):
    tail_number = models.CharField(max_length=20, unique=True)
    aircraft_type = models.CharField(max_length=100)
    capacity = models.IntegerField()
    speed = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='active')  # для запроса №4
    
    def __str__(self):
        return f"{self.tail_number} ({self.aircraft_type})"


# Аэропорт
class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.code} - {self.city}"


# Сотрудник
class Employee(models.Model):
    POSITION_CHOICES = [
        ('captain', 'Командир'),
        ('copilot', 'Второй пилот'),
        ('navigator', 'Штурман'),
        ('steward', 'Стюард/Стюардесса'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    education = models.CharField(max_length=100)
    experience = models.IntegerField()
    passport = models.CharField(max_length=50)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES) # должность
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_position_display()})"


# Экипаж (Crew)
class Crew(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Экипаж {self.name}"


# Член экипажа (связь сотрудника с экипажем)
class CrewMember(models.Model):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='members')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)  # допуск к рейсу
    
    class Meta:
        unique_together = ['crew', 'employee']
    
    def __str__(self):
        return f"{self.employee} в {self.crew}"


# Рейс
class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    distance = models.IntegerField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    tickets_sold = models.IntegerField(default=0)
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True, blank=True, related_name='flights')
    
    def __str__(self):
        return f"Рейс {self.flight_number}"
    
    # Свойства для получения конкретных членов экипажа по должности
    @property
    def captain(self):
        """Командир корабля"""
        if self.crew:
            member = self.crew.members.filter(employee__position='captain').first()
            return member.employee if member else None
        return None
    
    @property
    def copilot(self):
        """Второй пилот"""
        if self.crew:
            member = self.crew.members.filter(employee__position='copilot').first()
            return member.employee if member else None
        return None
    
    @property
    def navigator(self):
        """Штурман"""
        if self.crew:
            member = self.crew.members.filter(employee__position='navigator').first()
            return member.employee if member else None
        return None
    
    @property
    def stewards(self):
        """Стюарды/стюардессы"""
        if self.crew:
            return self.crew.members.filter(employee__position='steward')
        return CrewMember.objects.none()

    @property
    def crew_info(self):
        """Вся информация об экипаже"""
        if not self.crew:
            return None
        crew_data = {
            'crew_name': self.crew.name,
            'members': []
        }
        for member in self.crew.members.all():
            crew_data['members'].append({
                'employee_id': member.employee.id,
                'name': f"{member.employee.last_name} {member.employee.first_name}",
                'position': member.employee.get_position_display(),
                'is_approved': member.is_approved
            })
        return crew_data


# Транзитная остановка
class TransitStop(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='transit_stops')
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    arrival_datetime = models.DateTimeField()
    departure_datetime = models.DateTimeField()
    
    def __str__(self):
        return f"{self.flight.flight_number} - {self.airport.code}"
