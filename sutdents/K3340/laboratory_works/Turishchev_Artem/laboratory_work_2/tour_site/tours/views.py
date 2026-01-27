from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q, Count, Avg
from .models import Tour, Reservation, Review
from .forms import UserRegisterForm, ReviewForm, ReserveForm

TEMPLATES_DIR = 'tours/'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, f'{TEMPLATES_DIR}register.html', {'form': form})

class TourListView(ListView):
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Tour.objects.all().annotate(
            average_rating=Avg('review__rating')
        )
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(agency__icontains=search_query)
            )
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        if form.is_valid():
            reserve = form.save(commit=False)
            reserve.tour = tour
            reserve.user = request.user
            reserve.save()
            messages.success(request, 'Тур забронирован')
            return redirect('my_reservations')
    else:
        form = ReserveForm()
    return render(request, f'{TEMPLATES_DIR}reserve_confirm.html', {'tour': tour, 'form': form})

@login_required
def change_tour(request, tour_id, reservation_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReserveForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.reservation_approve = False
            reservation.save()
            messages.success(request, 'Тур Изменен')
            return redirect('my_reservations')
    else:
        form = ReserveForm(instance=reservation)
    return render(request, f'{TEMPLATES_DIR}reserve_confirm.html', {'tour': tour, 'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, f'{TEMPLATES_DIR}my_reservations.html', {'reservations': reservations})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    messages.success(request, 'Бронирование удалено.')
    return redirect('my_reservations')

@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен')
            return redirect('tour_list')
    else:
        form = ReviewForm()
    return render(request, f'{TEMPLATES_DIR}add_review.html', {'tour': tour, 'form': form})

def sold_tours_by_country(request):
    data = Tour.objects.filter(reservation__isnull=False).values('country').annotate(count=Count('id')).order_by('-count')
    total_count = sum(item['count'] for item in data)
    return render(request, f'{TEMPLATES_DIR}sold_tours.html', {'data': data, 'total_count': total_count})

def tour_reviews(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')
    
    if reviews.exists():
        from django.db.models import Avg
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        tour.average_rating = avg_rating
    else:
        tour.average_rating = None
    
    return render(request, 'tours/tour_reviews.html', {'tour': tour, 'reviews': reviews})