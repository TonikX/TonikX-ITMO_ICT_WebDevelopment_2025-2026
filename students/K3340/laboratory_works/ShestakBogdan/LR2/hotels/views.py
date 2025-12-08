from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import Hotel, Room, Reservation, Review
from .forms import ReservationForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

def hotels_list(request):
    qs = Hotel.objects.prefetch_related("amenities", "room_types")
    return render(request, "hotels/list.html", {"hotels": qs})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.rooms.select_related("room_type")
    reviews = []
    for room in rooms:
        reviews += list(room.reviews.all())

    return render(request, "hotels/detail.html", {
        "hotel": hotel,
        "rooms": rooms,
        "reviews": reviews
})

@login_required
def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]
            # availability check
            conflict = room.reservations.filter(
                status__in=["reserved", "checked_in"],
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exists()
            if conflict:
                messages.error(request, "Номер в эти даты занят.")
            else:
                r = form.save(commit=False)
                r.user = request.user
                r.room = room
                r.save()
                messages.success(request, "Резерв создан.")
                return redirect("my_reservations")
    else:
        form = ReservationForm()
    return render(request, "hotels/reserve.html", {"form": form, "room": room})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('room', 'room__hotel')
    return render(request, 'hotels/my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, pk):
    r = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == "POST":
        r.status = "cancelled"
        r.save()
        messages.success(request, "Резерв отменён.")
        return redirect("my_reservations")
    return render(request, "hotels/cancel_confirm.html", {"reservation": r})

@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            check_in = form.cleaned_data["check_in"]
            check_out = form.cleaned_data["check_out"]

            # Проверяем, не пересекается ли новая бронь с другими
            conflict = Reservation.objects.filter(
                room=reservation.room,
                status__in=["reserved", "checked_in"],
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exclude(pk=reservation.pk).exists()

            if conflict:
                messages.error(request, "Этот номер уже занят в выбранные даты.")
            else:
                form.save()
                messages.success(request, "Бронирование успешно обновлено.")
                return redirect("my_reservations")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "hotels/edit_reservation.html", {"form": form, "reservation": reservation})

@login_required
def write_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.room = room
            rev.save()
            messages.success(request, "Отзыв добавлен.")
            return redirect("hotel_detail", pk=room.hotel.id)
    else:
        form = ReviewForm()
    return render(request, "hotels/review.html", {"form": form, "room": room})

def occupants_last_month(request):
    now = timezone.localdate()
    month_ago = now - timedelta(days=30)
    qs = Reservation.objects.filter(
        check_in__lte=now,
        check_out__gte=month_ago,
        status__in=["reserved", "checked_in", "checked_out"]
    ).select_related("room__hotel", "user")
    by_hotel = qs.values("room__hotel__id", "room__hotel__name").annotate(
        guests_count=Count("user", distinct=True),
        total_reservations=Count("id")
    ).order_by("-guests_count")
    return render(request, "hotels/occupants.html", {"by_hotel": by_hotel, "qs": qs})

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
# Create your views here.
