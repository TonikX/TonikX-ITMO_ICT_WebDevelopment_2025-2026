from django.shortcuts import render, redirect
from .forms import HotelUserCreationForm
from .models import Hotel, Review, RoomType
from django.db.models import Avg


def register(request):
    if request.method == "POST":
        form = HotelUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем на страницу логина
    else:
        form = HotelUserCreationForm()
    return render(request, 'register.html', {'form': form})

def hotels(request):
    h = Hotel.objects.all()

    # average_rating = Review.objects.filter(
    #     id_reservation__id_room__id_hotel=1
    # ).aggregate(avg_rating=Avg('raiting'))['avg_rating']
    return render(request, 'hotels_cards.html', {'hotels': h})

def all_rooms(request):
    pk = request.GET.get('id')
    if pk:
        rooms = RoomType.objects.filter(id_hotel=pk)
    else:
        rooms = RoomType.objects.all()
    return render(request, 'all_rooms.html', {"rooms": rooms})

def book_room(request, pk):
    room = RoomType.objects.filter(pk=pk).first()
    return render(request, 'book_room.html', {"room": room})

def room_info(request, pk):
    room = RoomType.objects.filter(pk=pk).first()
    return render(request, 'room_info.html', {"room": room})

def home(request):
    return render(request, 'home.html')