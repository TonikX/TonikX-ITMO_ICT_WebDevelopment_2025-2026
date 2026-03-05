from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from .models import Tour, Review
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def dispatch(self, request, *args, **kwargs):
        self.tour = get_object_or_404(Tour, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tour = self.tour
        form.instance.author = self.request.user
        form.instance.tour_start_date = self.tour.start_date
        form.instance.tour_end_date = self.tour.end_date
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tours:detail", kwargs={"pk": self.tour.pk})
