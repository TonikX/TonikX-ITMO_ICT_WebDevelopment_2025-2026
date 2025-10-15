from django.db.models import Avg
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import HotelUserCreationForm, ReservationForm
from .models import Hotel, Review, RoomType
from .models import Reservation, RoomType
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy


def register(request):
    if request.method == "POST":
        form = HotelUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = HotelUserCreationForm()
    return render(request, 'register.html', {'form': form})

def hotels(request):
    h = Hotel.objects.all()
    hotels_with_rating = []
    for i in h:
        hotels_with_rating.append({'hotel': i, 'rating': Review.objects.filter(
            id_reservation__id_rooms__id_hotel=i.pk
        ).aggregate(avg_rating=Avg('rating'))['avg_rating']})

    return render(request, 'hotels_cards.html', {'hotels_with_rating': hotels_with_rating})

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

@login_required
def reservations(request):
    r = Reservation.objects.filter(id_user=request.user)
    return render(request, 'reservations.html', {'reservations': r})


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'
    success_url = reverse_lazy('reservations')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.get_object().id_rooms
        return kwargs

    def get_object(self, queryset=None):
        reservation = super().get_object(queryset)
        if reservation.id_user != self.request.user:
            return HttpResponseForbidden("Вы не можете редактировать чужое бронирование")
        return reservation


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.get_object().id_rooms
        return kwargs

    def test_func(self):
        reservation = self.get_object()
        return reservation.id_user == self.request.user



# class ReservationCreateView(CreateView):
#     model = Reservation
#     form_class = ReservationForm
#     template_name = 'reservation_form.html'
#     success_url = reverse_lazy('home')
#
#     def form_valid(self, form):
#         form.instance.id_user = self.request.user
#         return super().form_valid(form)