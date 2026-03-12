from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Hotel, Room, Reservation, Review
from .forms import ReservationForm, ReviewForm
from datetime import timedelta
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

def hotels_list(request):
    return render(request, "hotels/list.html", {"hotels": Hotel.objects.all()})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, "hotels/detail.html", {
        "hotel": hotel,
        "rooms": Room.objects.filter(hotel=hotel),
        "reviews": Review.objects.filter(room__hotel=hotel)
    })


@login_required
def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            if check_in >= check_out:
                messages.error(request, 'Дата выезда должна быть позже даты заезда')
                return render(request, "hotels/reserve.html", {"form": form, "room": room})

            if check_in < timezone.now().date():
                messages.error(request, 'Дата заезда не может быть в прошлом')
                return render(request, "hotels/reserve.html", {"form": form, "room": room})

            conflicting_reservations = Reservation.objects.filter(
                room=room,
                status__in=['reserved', 'checked_in'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )

            if conflicting_reservations.exists():
                messages.error(request, 'Номер уже забронирован на выбранные даты')
                return render(request, "hotels/reserve.html", {"form": form, "room": room})

            r = form.save(commit=False)
            r.user, r.room = request.user, room
            r.save()
            messages.success(request, "Резерв создан.")
            return redirect("my_reservations")
    else:
        form = ReservationForm()
    return render(request, "hotels/reserve.html", {"form": form, "room": room})


@login_required
def my_reservations(request):
    return render(request, 'hotels/my_reservations.html', {
        'reservations': Reservation.objects.filter(user=request.user)
    })


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
    r = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=r)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            if check_in >= check_out:
                messages.error(request, 'Дата выезда должна быть позже даты заезда')
                return render(request, "hotels/edit_reservation.html", {"form": form, "reservation": r})

            if check_in < timezone.now().date():
                messages.error(request, 'Дата заезда не может быть в прошлом')
                return render(request, "hotels/edit_reservation.html", {"form": form, "reservation": r})

            conflicting_reservations = Reservation.objects.filter(
                room=r.room,
                status__in=['reserved', 'checked_in'],
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exclude(pk=pk)

            if conflicting_reservations.exists():
                messages.error(request, 'Номер уже забронирован на выбранные даты')
                return render(request, "hotels/edit_reservation.html", {"form": form, "reservation": r})

            form.save()
            messages.success(request, "Бронирование обновлено.")
            return redirect("my_reservations")
    else:
        form = ReservationForm(instance=r)
    return render(request, "hotels/edit_reservation.html", {"form": form, "reservation": r})


@login_required
def write_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user, rev.room = request.user, room
            rev.save()
            messages.success(request, "Отзыв добавлен.")
            return redirect("hotel_detail", pk=room.hotel.id)
    else:
        form = ReviewForm()
    return render(request, "hotels/review.html", {"form": form, "room": room})


@staff_member_required
def occupants_last_month(request):
    now = timezone.localdate()
    month_ago = now - timedelta(days=30)

    # Бронирования за последний месяц
    reservations = Reservation.objects.filter(
        check_in__lte=now,
        check_out__gte=month_ago
    ).select_related('user', 'room__hotel').order_by('-check_in')

    # Статистика по отелям
    by_hotel = reservations.values(
        'room__hotel__id',
        'room__hotel__name'
    ).annotate(
        guests_count=Count('user', distinct=True),
        total_reservations=Count('id')
    ).order_by('room__hotel__name')

    # Общая статистика
    total_unique_guests = reservations.values('user').distinct().count()
    total_reservations = reservations.count()

    context = {
        'by_hotel': by_hotel,
        'reservations': reservations,
        'total_unique_guests': total_unique_guests,
        'total_reservations': total_reservations,
        'now': now,
        'month_ago': month_ago
    }
    return render(request, "hotels/occupants.html", context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')