from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Hotel, Room, Booking, Review
from .forms import (
    UserRegistrationForm, BookingForm, ReviewForm,
    HotelFilterForm, RoomFilterForm
)
from .services import get_available_rooms, get_recent_guests
from datetime import date


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация успешна! Войдите в систему.')
        return super().form_valid(form)


class HotelListView(ListView):
    model = Hotel
    template_name = 'booking/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 10

    def get_queryset(self):
        queryset = Hotel.objects.all()
        form = HotelFilterForm(self.request.GET)

        if form.is_valid():
            search = form.cleaned_data.get('search')
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(address__icontains=search)
                )

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = HotelFilterForm(self.request.GET)
        return context


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'booking/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = self.object.room_types.prefetch_related('amenities', 'rooms')

        if self.request.user.is_staff or (
                self.request.user.is_authenticated and self.request.user == self.object.owner):
            context['recent_guests'] = get_recent_guests(self.object, days=30)
        else:
            context['recent_guests'] = None

        reviews = Review.objects.filter(
            room__room_type__hotel=self.object
        ).select_related('user', 'room', 'booking').order_by('-created_at')[:10]
        context['reviews'] = reviews

        avg_rating = Review.objects.filter(
            room__room_type__hotel=self.object
        ).aggregate(Avg('rating'))['rating__avg'] # 4.3
        context['average_rating'] = round(avg_rating, 1) if avg_rating else None

        return context


class RoomListView(ListView):
    model = Room
    template_name = 'booking/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 12

    def get_queryset(self):
        queryset = Room.objects.filter(is_active=True).select_related(
            'room_type__hotel'
        ).prefetch_related('room_type__amenities')

        hotel_id = self.kwargs.get('hotel_id')
        if hotel_id:
            queryset = queryset.filter(room_type__hotel_id=hotel_id)

        form = RoomFilterForm(self.request.GET)

        if form.is_valid():
            room_type = form.cleaned_data.get('room_type')
            amenities = form.cleaned_data.get('amenities')
            min_capacity = form.cleaned_data.get('min_capacity')
            max_price = form.cleaned_data.get('max_price')
            check_in = form.cleaned_data.get('check_in')
            check_out = form.cleaned_data.get('check_out')

            if room_type:
                queryset = queryset.filter(room_type=room_type)

            if amenities:
                for amenity in amenities:
                    queryset = queryset.filter(room_type__amenities=amenity)

            if min_capacity:
                queryset = queryset.filter(room_type__capacity__gte=min_capacity)

            if max_price:
                queryset = queryset.filter(room_type__price_per_night__lte=max_price)

            if check_in and check_out:
                available_rooms = get_available_rooms(check_in, check_out)
                queryset = queryset.filter(id__in=available_rooms.values_list('id', flat=True))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hotel_id = self.kwargs.get('hotel_id')
        if hotel_id:
            context['hotel'] = get_object_or_404(Hotel, pk=hotel_id)
            context['filter_form'] = RoomFilterForm(self.request.GET, hotel_id=hotel_id)
        else:
            context['filter_form'] = RoomFilterForm(self.request.GET)

        return context


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        hotel_id = self.request.GET.get('hotel')
        if hotel_id:
            kwargs['hotel_id'] = hotel_id

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room')
        if room_id:
            initial['room'] = room_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel_id = self.request.GET.get('hotel')
        if hotel_id:
            context['hotel'] = get_object_or_404(Hotel, pk=hotel_id)

        room_id = self.request.GET.get('room')
        if room_id:
            context['room'] = get_object_or_404(Room, pk=room_id)

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование успешно создано!')
        return super().form_valid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('my_bookings')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.can_edit:
            messages.error(self.request, 'Это бронирование нельзя редактировать')
            return redirect('my_bookings')
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование обновлено!')
        return super().form_valid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    success_url = reverse_lazy('my_bookings')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.can_cancel:
            messages.error(self.request, 'Это бронирование нельзя отменить')
            return redirect('my_bookings')
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'cancelled'
        self.object.save()
        messages.success(request, 'Бронирование отменено')
        return redirect(self.success_url)


class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'room__room_type__hotel'
        ).order_by('-created_at')


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            'room__room_type__hotel'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_review'] = Review.objects.filter(
            booking=self.object,
            user=self.request.user
        ).exists()
        context['can_review'] = (
                self.object.check_in <= date.today() and
                self.object.status in ['checked_in', 'checked_out']
        )
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'booking/review_form.html'
    success_url = reverse_lazy('my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        booking_id = self.kwargs.get('booking_id')
        booking = get_object_or_404(Booking, pk=booking_id, user=self.request.user)
        kwargs['booking'] = booking

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        context['booking'] = get_object_or_404(Booking, pk=booking_id, user=self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв успешно добавлен!')
        return super().form_valid(form)


class MyReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'booking/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related(
            'room__room_type__hotel', 'booking'
        ).order_by('-created_at')


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'booking/review_form.html'
    success_url = reverse_lazy('my_reviews')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['booking'] = self.object.booking
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв обновлён!')
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'booking/review_confirm_delete.html'
    success_url = reverse_lazy('my_reviews')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отзыв удалён')
        return super().delete(request, *args, **kwargs)