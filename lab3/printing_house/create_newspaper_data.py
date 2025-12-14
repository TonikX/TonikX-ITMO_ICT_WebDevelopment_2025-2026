#!/usr/bin/env python
"""
Скрипт для создания тестовых данных для системы распределения газет
"""
import os
import sys
import django
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printing_house.settings')
django.setup()

from core.models import (
    Newspaper, PrintingHouse, PostOffice, PrintingRun, Distribution
)


def create_sample_data():
    """Создание тестовых данных для системы газет"""
    
    # Газеты
    newspaper1 = Newspaper.objects.create(
        title='Городские вести',
        publication_index='GV-001',
        editor_first_name='Иван',
        editor_last_name='Иванов',
        editor_middle_name='Иванович',
        price_per_copy=Decimal('25.00')
    )
    
    newspaper2 = Newspaper.objects.create(
        title='Новости дня',
        publication_index='ND-002',
        editor_first_name='Петр',
        editor_last_name='Петров',
        editor_middle_name='Петрович',
        price_per_copy=Decimal('30.00')
    )
    
    newspaper3 = Newspaper.objects.create(
        title='Спортивная жизнь',
        publication_index='SL-003',
        editor_first_name='Анна',
        editor_last_name='Смирнова',
        editor_middle_name='Владимировна',
        price_per_copy=Decimal('35.00')
    )
    
    newspaper4 = Newspaper.objects.create(
        title='Экономические новости',
        publication_index='EN-004',
        editor_first_name='Михаил',
        editor_last_name='Козлов',
        editor_middle_name='Сергеевич',
        price_per_copy=Decimal('40.00')
    )
    
    newspaper5 = Newspaper.objects.create(
        title='Культурный обзор',
        publication_index='KO-005',
        editor_first_name='Ольга',
        editor_last_name='Волкова',
        editor_middle_name='Александровна',
        price_per_copy=Decimal('28.00')
    )
    
    # Типографии
    ph1 = PrintingHouse.objects.create(
        name='Типография "Печатный дом"',
        address='г. Москва, ул. Промышленная, д. 15',
        is_active=True
    )
    
    ph2 = PrintingHouse.objects.create(
        name='Типография "Книга"',
        address='г. Москва, ул. Типографская, д. 8',
        is_active=True
    )
    
    ph3 = PrintingHouse.objects.create(
        name='Типография "Современник"',
        address='г. Санкт-Петербург, пр. Невский, д. 100',
        is_active=True
    )
    
    ph4 = PrintingHouse.objects.create(
        name='Типография "Старая типография"',
        address='г. Москва, ул. Старая, д. 5',
        is_active=False  # Закрыта
    )
    
    # Почтовые отделения
    po1 = PostOffice.objects.create(
        number='101001',
        address='г. Москва, ул. Тверская, д. 1'
    )
    
    po2 = PostOffice.objects.create(
        number='101002',
        address='г. Москва, ул. Арбат, д. 25'
    )
    
    po3 = PostOffice.objects.create(
        number='101003',
        address='г. Москва, ул. Ленина, д. 10'
    )
    
    po4 = PostOffice.objects.create(
        number='191001',
        address='г. Санкт-Петербург, Невский пр., д. 50'
    )
    
    po5 = PostOffice.objects.create(
        number='191002',
        address='г. Санкт-Петербург, ул. Садовая, д. 15'
    )
    
    # Тиражи (связь типографий и газет)
    PrintingRun.objects.create(
        printing_house=ph1,
        newspaper=newspaper1,
        circulation=10000
    )
    
    PrintingRun.objects.create(
        printing_house=ph1,
        newspaper=newspaper2,
        circulation=15000
    )
    
    PrintingRun.objects.create(
        printing_house=ph1,
        newspaper=newspaper3,
        circulation=8000
    )
    
    PrintingRun.objects.create(
        printing_house=ph2,
        newspaper=newspaper1,
        circulation=5000
    )
    
    PrintingRun.objects.create(
        printing_house=ph2,
        newspaper=newspaper4,
        circulation=12000
    )
    
    PrintingRun.objects.create(
        printing_house=ph2,
        newspaper=newspaper5,
        circulation=7000
    )
    
    PrintingRun.objects.create(
        printing_house=ph3,
        newspaper=newspaper2,
        circulation=20000  # Самый большой тираж
    )
    
    PrintingRun.objects.create(
        printing_house=ph3,
        newspaper=newspaper3,
        circulation=6000
    )
    
    # Распределения (связь почтовых отделений, газет и типографий)
    
    # Газета "Городские вести" из разных типографий в разные почтовые отделения
    Distribution.objects.create(
        post_office=po1,
        newspaper=newspaper1,
        printing_house=ph1,
        quantity=500
    )
    
    Distribution.objects.create(
        post_office=po1,
        newspaper=newspaper1,
        printing_house=ph2,
        quantity=300
    )
    
    Distribution.objects.create(
        post_office=po2,
        newspaper=newspaper1,
        printing_house=ph1,
        quantity=400
    )
    
    # Газета "Новости дня"
    Distribution.objects.create(
        post_office=po1,
        newspaper=newspaper2,
        printing_house=ph1,
        quantity=600
    )
    
    Distribution.objects.create(
        post_office=po3,
        newspaper=newspaper2,
        printing_house=ph1,
        quantity=450
    )
    
    Distribution.objects.create(
        post_office=po4,
        newspaper=newspaper2,
        printing_house=ph3,
        quantity=800
    )
    
    # Газета "Спортивная жизнь"
    Distribution.objects.create(
        post_office=po2,
        newspaper=newspaper3,
        printing_house=ph1,
        quantity=350
    )
    
    Distribution.objects.create(
        post_office=po5,
        newspaper=newspaper3,
        printing_house=ph3,
        quantity=200  # Малое количество
    )
    
    # Газета "Экономические новости"
    Distribution.objects.create(
        post_office=po3,
        newspaper=newspaper4,
        printing_house=ph2,
        quantity=500
    )
    
    Distribution.objects.create(
        post_office=po1,
        newspaper=newspaper4,
        printing_house=ph2,
        quantity=150  # Малое количество
    )
    
    # Газета "Культурный обзор"
    Distribution.objects.create(
        post_office=po2,
        newspaper=newspaper5,
        printing_house=ph2,
        quantity=250
    )
    
    Distribution.objects.create(
        post_office=po4,
        newspaper=newspaper5,
        printing_house=ph2,
        quantity=180  # Малое количество
    )
    
    print(f"\nСоздано:")
    print(f"- Газет: {Newspaper.objects.count()}")
    print(f"- Типографий: {PrintingHouse.objects.count()}")
    print(f"- Почтовых отделений: {PostOffice.objects.count()}")
    print(f"- Тиражей: {PrintingRun.objects.count()}")
    print(f"- Распределений: {Distribution.objects.count()}")


if __name__ == '__main__':
    create_sample_data()

