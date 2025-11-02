from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Hotel, RoomType, Reservation, Review
from .forms import CustomUserCreationForm, ReservationForm, ReviewForm, EditReservationForm
from .mixins import ReservationEditableMixin, ReviewAllowedMixin

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'hotel_management/login.html'
    success_message = "Вы успешно вошли в систему!"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'hotel_management/register.html'
    success_url = reverse_lazy('hotel_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно!')
        return response

# Доступно без авторизации
class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel_management/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 2

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel_management/hotel_detail.html'
    context_object_name = 'hotel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = RoomType.objects.filter(hotel=self.object).distinct()
        return context

class RoomTypeDetailView(DetailView):
    model = RoomType
    template_name = 'hotel_management/room_type_detail.html'
    context_object_name = 'room_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        reviews = Review.objects.filter(
            reservation__room__type=self.object
        ).select_related('reservation__user').order_by('-created_at')
        
        context['reviews'] = reviews
        
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            context['average_rating'] = round(total_rating / len(reviews), 1)
            context['reviews_count'] = len(reviews)
        else:
            context['average_rating'] = 0
            context['reviews_count'] = 0
            
        return context


class MakeReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'hotel_management/make_reservation.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.room_type = get_object_or_404(RoomType, id=self.kwargs['room_type_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room_type'] = self.room_type
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Бронирование создано успешно!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_type'] = self.room_type
        return context
    
    def get_success_url(self):
        return reverse_lazy('my_reservations')

class MyReservationsListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'hotel_management/my_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')


class EditReservationView(LoginRequiredMixin, ReservationEditableMixin, UpdateView):
    model = Reservation
    form_class = EditReservationForm
    template_name = 'hotel_management/edit_reservation.html'
    context_object_name = 'reservation'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['reservation'] = self.object
        return kwargs
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Бронирование обновлено успешно!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('my_reservations')
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class DeleteReservationView(LoginRequiredMixin, ReservationEditableMixin, DeleteView):
    model = Reservation
    template_name = 'hotel_management/delete_reservation.html'
    context_object_name = 'reservation'
    
    def form_valid(self, form):
        messages.success(self.request, 'Бронирование удалено успешно!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('my_reservations')


class AddReviewView(LoginRequiredMixin, ReviewAllowedMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'hotel_management/add_review.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.reservation = get_object_or_404(
            Reservation, 
            id=self.kwargs['reservation_id']
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.reservation = self.reservation
        response = super().form_valid(form)
        messages.success(self.request, 'Отзыв добавлен успешно!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservation'] = self.reservation
        return context
    
    def get_success_url(self):
        return reverse_lazy('my_reservations')


class GuestsLastMonthView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Reservation
    template_name = 'hotel_management/guests_last_month.html'
    context_object_name = 'guests'

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        messages.error(self.request, "Доступ к этой странице разрешен только персоналу отеля.")
        return redirect('hotel_list')
    
    def get_queryset(self):
        one_month_ago = timezone.now() - timedelta(days=30)
        return Reservation.objects.filter(
            check_in__gte=one_month_ago,
            status__in=['checked_in', 'checked_out']
        ).select_related('user', 'room__type', 'room__type__hotel').order_by('-check_in')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['period'] = (timezone.now() - timedelta(days=30)).date()
        return context