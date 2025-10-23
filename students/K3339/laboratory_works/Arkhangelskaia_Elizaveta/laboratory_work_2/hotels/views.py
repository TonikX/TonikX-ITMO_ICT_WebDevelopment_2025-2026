from django.core.paginator import Paginator

from .forms import HotelUserCreationForm, ReservationForm, ReviewForm
from .models import Facility, Hotel, Reservation, Review, RoomType
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, UpdateView


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
        hotels_with_rating.append({
            'hotel': i,
            'rating': round(
                Review.objects.filter(
                    id_reservation__id_rooms__id_hotel=i.pk
                ).aggregate(
                    avg_rating=Avg('rating'))['avg_rating'], 1)
        })

    return render(request,
                  'hotels_cards.html',
                  {'hotels_with_rating': hotels_with_rating})

def all_rooms(request):
    pk = request.GET.get('id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if pk:
        rooms = RoomType.objects.filter(id_hotel=pk).select_related('id_hotel')
        hotel_name = Hotel.objects.get(pk=pk).name
    else:
        rooms = RoomType.objects.all().select_related('id_hotel')
        hotel_name = None

    all_hotels = Hotel.objects.all()
    if checkin and checkout:
        rooms = rooms.annotate(
            overlapping_reservations=Count(
                'reservation',
                filter=~Q(reservation__end_date__lte=checkin) & ~Q(reservation__start_date__gte=checkout))
        ).annotate(
            available_count=F('count') - F('overlapping_reservations')
        ).filter(available_count__gt=0)

    rooms_with_facility_and_review = []
    for i in rooms:
        facilities = Facility.objects.filter(id_room_type=i.pk)
        reviews = Review.objects.filter(
            id_reservation__id_rooms=i.pk
        ).select_related(
            'id_reservation', 'id_reservation__id_user'
        )
        rooms_with_facility_and_review += [{'room': i, 'facilities': facilities, 'reviews': reviews}]

    return render(request, 'all_rooms.html', {
        "rooms": rooms_with_facility_and_review,
        "hotel_name": hotel_name,
        "all_hotels": all_hotels,
        "checkin": checkin,
        "checkout": checkout
    })


@login_required
def book_room(request, pk):
    room = get_object_or_404(RoomType, pk=pk)
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        num_people = int(request.POST.get('num_people'))
        today = str(timezone.now().date())

        if not checkin or not checkout:
            messages.error(request, "Выберите даты заезда и выезда.")
        elif checkin >= checkout:
            messages.error(request, "Дата выезда должна быть позже даты заезда.")
        elif not (today <= checkin and today<= checkout):
            messages.error(request, "Нельзя выбрать прошедшие даты.")
        elif num_people > room.capacity:
            messages.error(request, f"Номер рассчитан максимум на {room.capacity} гостей.")
        else:
            rooms = RoomType.objects.filter(pk=pk).annotate(
                overlapping_reservations=Count(
                    'reservation',
                    filter=~Q(reservation__end_date__lte=checkin) & ~Q(reservation__start_date__gte=checkout)
                )
            ).annotate(
                available_count=F('count') - F('overlapping_reservations')
            ).filter(available_count__gt=0)

            if rooms:
                Reservation.objects.create(
                    id_user=request.user,
                    id_rooms=room,
                    start_date=checkin,
                    end_date=checkout,
                    reservation_date=timezone.now()
                )
            else:
                messages.error(request, "На эти даты номер занят!!")
            return redirect('reservations')

    return render(request,
                  'book_room.html',
                  {'room': room,
                   'checkin': checkin,
                   'checkout': checkout})

def home(request):
    return redirect('hotels')


@login_required
def reservations(request):
    r = Reservation.objects.filter(
        id_user=request.user
    ).select_related('id_rooms', 'id_rooms__id_hotel', 'review' )
    future, past, now = [], [], []
    today = timezone.now().date()

    for i in r:
        if today < i.start_date :
            future.append(i)
        elif i.start_date <= today <= i.end_date:
            now.append(i)
        else:
            past.append(i)

    return render(request,'reservations.html',
                  {'past_reservations': past,
                   'future_reservations': future,
                   'now_reservations': now
                   })


def last_month_guests(request):
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)

    r = Reservation.objects.filter(
        start_date__gte=month_ago,
        start_date__lte=today
    ).select_related('id_user', 'id_rooms__id_hotel')

    paginator = Paginator(r, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'last_month_guests.html', {'page_obj': page_obj})


def custom_logout(request):
    logout(request)
    return redirect('login')

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

    def form_valid(self, form):
        reservation = form.instance
        room = reservation.id_rooms
        checkin = form.cleaned_data['start_date']
        checkout = form.cleaned_data['end_date']
        today = timezone.now().date()
        if checkin < today:
            form.add_error(None, "Нельзя выбрать прошедшую дату")
            return self.form_invalid(form)

        rooms_available = RoomType.objects.filter(pk=room.pk).annotate(
            overlapping_reservations=Count(
                'reservation',
                filter=~Q(reservation__end_date__lte=checkin) & ~Q(reservation__start_date__gte=checkout)
            )
        ).annotate(
            available_count=F('count') - F('overlapping_reservations')
        ).filter(available_count__gt=0)

        if not rooms_available.exists():
            form.add_error(None, "Номер занят на выбранные даты")
            return self.form_invalid(form)

        return super().form_valid(form)


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations')


    def test_func(self):
        reservation = self.get_object()
        return reservation.id_user == self.request.user and reservation.start_date > timezone.now().date()


@login_required
def get_review(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, id_user=request.user)

    if Review.objects.filter(id_reservation=reservation).exists():
        messages.warning(request, "Вы уже оставили отзыв для этого бронирования.")
        return redirect('reservations')

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.id_reservation = reservation
            review.save()
            return redirect('reservations')
    else:
        form = ReviewForm()

    return render(request,
                  'get_review.html',
                  {'form': form, 'reservation': reservation})
