from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from datetime import date, timedelta
from .models import Hotel, Room, Reservation, RoomType, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ReservationForm, ReviewForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotels_list')
    else:
        form = UserCreationForm()
    return render(request, 'hotels_app/register.html', {'form': form})


def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels_app/hotel_list.html', {'hotels': hotels})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'hotels_app/hotel_detail.html', {'hotel': hotel})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    review_reservation = None
    if request.user.is_authenticated:
        review_reservation = Reservation.objects.filter(
            user=request.user,
            room=room,
            status='checked_out'
        ).exclude(reviews__isnull=False).order_by('-date_to').first()
    return render(request, 'hotels_app/room_detail.html', {'room': room, 'review_reservation': review_reservation})


@login_required
def create_reservation(request):
    room = None
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            room_instance = form.cleaned_data.get('room')
            if not room_instance:
                return render(request, 'hotels_app/reservation_error.html', {'message': 'Комната не выбрана.', 'room': None})            
            overlaps = Reservation.objects.filter(
                room=room_instance,
                date_from__lte=form.cleaned_data['date_to'],
                date_to__gte=form.cleaned_data['date_from']
            )
            if overlaps.exists():
                return render(request, 'hotels_app/reservation_error.html', {'message': 'Комната занята в эти даты.', 'room': room_instance})
            res = Reservation(
                user=request.user,
                room=room_instance,
                date_from=form.cleaned_data['date_from'],
                date_to=form.cleaned_data['date_to']
            )
            res.save()
            return redirect('my_reservations')
        else:
            room = form.cleaned_data.get('room') if 'room' in form.cleaned_data else None
    else:
        initial = {}
        room_id = request.GET.get('room')
        if room_id:
            room = get_object_or_404(Room, pk=room_id)
            initial['room'] = room_id
        form = ReservationForm(initial=initial)
    return render(request, 'hotels_app/reservation_form.html', {'form': form, 'room': room})


@login_required
def my_reservations(request):
    if request.user.is_staff:
        reservations = Reservation.objects.all().order_by('-date_from')
    else:
        reservations = Reservation.objects.filter(user=request.user).order_by('-date_from')

    return render(request, 'hotels_app/my_reservations.html', {'reservations': reservations})


@staff_member_required
def reservation_checkin(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.status = 'checked_in'
    res.save()
    return redirect('my_reservations')


@staff_member_required
def reservation_checkout(request, pk):
    res = get_object_or_404(Reservation, pk=pk)
    res.status = 'checked_out'
    res.save()
    return redirect('my_reservations')


@login_required
def edit_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk, user=request.user)
    room = res.room
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=res)
        if form.is_valid():
            updated = form.save(commit=False)
            overlaps = Reservation.objects.filter(
                room=updated.room,
                date_from__lte=updated.date_to,
                date_to__gte=updated.date_from
            ).exclude(pk=res.pk)
            if overlaps.exists():
                return render(request, 'hotels_app/reservation_error.html', {'message': 'Комната занята в эти даты.', 'room': updated.room})
            updated.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=res)
    return render(request, 'hotels_app/reservation_form.html', {'form': form, 'editing': True, 'room': room})


@login_required
def cancel_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        res.delete()
        return redirect('my_reservations')
    return render(request, 'hotels_app/reservation_cancel.html', {'reservation': res})


@login_required
def reservation_review(request, pk):
    res = get_object_or_404(Reservation, pk=pk, user=request.user, status='checked_out')
    if res.reviews.exists():
        return redirect('room_detail', pk=res.room.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.room = res.room
            rev.reservation = res
            if not rev.period_from:
                rev.period_from = res.date_from
            if not rev.period_to:
                rev.period_to = res.date_to
            rev.save()
            return redirect('my_reservations')
    else:
        initial = {'period_from': res.date_from, 'period_to': res.date_to}
        form = ReviewForm(initial=initial)
    return render(request, 'hotels_app/review_form.html', {'form': form, 'reservation': res})


@login_required
def add_review(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.room = room
            recent = Reservation.objects.filter(user=request.user, room=room).order_by('-date_from').first()
            if recent:
                rev.reservation = recent
            rev.save()
            return redirect('room_detail', pk=room.pk)
    return redirect('room_detail', pk=room.pk)


class RoomListView(ListView):
    model = Room
    template_name = 'hotels_app/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 6

    def get_queryset(self):
        qs = Room.objects.select_related('hotel', 'room_type')
        q = self.request.GET.get('q')
        room_type = self.request.GET.get('type')
        if q:
            qs = qs.filter(hotel__name__icontains=q)
        if room_type:
            qs = qs.filter(room_type__id=room_type)
        return qs.order_by('price')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['room_types'] = RoomType.objects.all()
        return ctx


def guests_last_month(request):
    today = date.today()
    one_month_ago = today - timedelta(days=30)
    res = Reservation.objects.filter(date_to__gte=one_month_ago, date_from__lte=today)
    return render(request, 'hotels_app/guests_last_month.html', {'reservations': res})
