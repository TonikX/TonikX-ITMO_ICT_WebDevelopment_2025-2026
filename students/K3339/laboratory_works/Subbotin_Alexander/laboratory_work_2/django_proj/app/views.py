from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.views.generic.edit import FormMixin
from django.contrib import messages

from .models import Tour, Reservation
from .forms import ReviewForm, RegisterForm, ProfileForm


def register(request):
    if request.user.is_authenticated:
        return redirect('about')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("about")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        
        if not hasattr(user, 'profile'):
            from .models import UserProfile
            UserProfile.objects.create(user=user)
        
        if self.request.method == 'POST':
            form = ProfileForm(self.request.POST, instance=user.profile, user=user)
        else:
            form = ProfileForm(instance=user.profile, user=user)
        
        ctx['form'] = form
        return ctx
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        if not hasattr(user, 'profile'):
            from .models import UserProfile
            UserProfile.objects.create(user=user)
        
        form = ProfileForm(request.POST, instance=user.profile, user=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
        
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class TourListView(ListView):
    model = Tour
    template_name = 'tour_list.html'
    context_object_name = 'tours'
    paginate_by = 8
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                models.Q(title__icontains=q) |
                models.Q(agency__icontains=q) |
                models.Q(city__icontains=q) |
                models.Q(description__icontains=q)
            )
        return qs.order_by('start_date')
    

class MyReservationsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'my_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)



class TourDetailView(FormMixin, DetailView):
    model = Tour
    template_name = 'tour_detail.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        total_guests = self.object.reservations.filter(confirmed=True).aggregate(
            total=Sum('guests')
        )['total'] or 0
        
        ctx['total_guests'] = total_guests
        ctx['reservations_count'] = self.object.reservations.filter(confirmed=True).count()
        
        if self.request.user.is_authenticated:
            ctx['user_reservation'] = self.object.reservations.filter(user=self.request.user).first()
        
        return ctx

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите, чтобы оставить отзыв')
            return redirect('login')
        
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = self.object
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('tour_detail', pk=self.object.pk)
        else:
            messages.error(request, 'Ошибка при добавлении отзыва')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('tour_detail', kwargs={'pk': self.object.pk})


@login_required
def ReservationCreateView(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    existing = Reservation.objects.filter(user=request.user, tour=tour).exists()
    if not existing:
        Reservation.objects.create(
            user=request.user,
            tour=tour,
            confirmed=False,
            guests=1
        )
    return redirect('tour_detail', pk=tour_id)


class UserReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'my_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10


    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('tour').order_by('-created_at')


class ReservationOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        reservation = self.get_object()
        return reservation.user == self.request.user


class ReservationDeleteView(LoginRequiredMixin, ReservationOwnerMixin, DeleteView):
    model = Reservation
    template_name = 'reservation_confirm_delete.html'
    success_url = reverse_lazy('user_reservations')

class SoldByCityView(LoginRequiredMixin, TemplateView):
    template_name = 'sold_by_city.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        all_reservations = Tour.objects.filter(reservations__isnull=False).values('city').annotate(
            total_reservations=Count('reservations', distinct=True),
            total_guests=Sum('reservations__guests'),
            total_income=Sum(models.F('reservations__guests') * models.F('price'), output_field=models.DecimalField(max_digits=12, decimal_places=2))
        ).order_by('-total_reservations')

        confirmed_reservations = Tour.objects.filter(reservations__confirmed=True).values('city').annotate(
            confirmed_reservations=Count('reservations', distinct=True),
            confirmed_guests=Sum('reservations__guests'),
            confirmed_income=Sum(models.F('reservations__guests') * models.F('price'), output_field=models.DecimalField(max_digits=12, decimal_places=2))
        ).order_by('-confirmed_reservations')

        city_data = {}
        for item in all_reservations:
            city = item['city']
            city_data[city] = {
                'city': city,
                'total_reservations': item['total_reservations'],
                'total_guests': item['total_guests'],
                'total_income': item['total_income'],
                'confirmed_reservations': 0,
                'confirmed_guests': 0,
                'confirmed_income': 0
            }
        
        for item in confirmed_reservations:
            city = item['city']
            if city in city_data:
                city_data[city]['confirmed_reservations'] = item['confirmed_reservations']
                city_data[city]['confirmed_guests'] = item['confirmed_guests']
                city_data[city]['confirmed_income'] = item['confirmed_income']

        ctx['data'] = list(city_data.values())
        return ctx
    

class TourCreateView(UserPassesTestMixin, CreateView):
    model = Tour
    fields = ['title', 'agency', 'city', 'description', 'start_date', 'end_date', 'price', 'payment_terms']
    template_name = 'tour_form.html'
    success_url = reverse_lazy('tour_list')

    def test_func(self):
        return self.request.user.is_staff