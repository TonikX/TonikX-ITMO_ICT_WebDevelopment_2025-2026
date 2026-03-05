from django.views.generic import TemplateView
from django.db.models import Count, Sum
from .models import Booking

class SalesByCountryView(TemplateView):
    template_name = "bookings/sales_by_country.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        rows = (Booking.objects
                .filter(is_confirmed=True)
                .values("tour__country__name")
                .annotate(sold_count=Count("id"), total_revenue=Sum("tour__price"))
                .order_by("-sold_count", "tour__country__name"))
        ctx["rows"] = rows
        return ctx
