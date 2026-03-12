from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from .models import Tour, Review
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    '''метод dispatch вызывается первым при запросах GET, POST и т.д,
            он определяет, какой метод вызвать дальше'''
    def dispatch(self, request, *args, **kwargs):
        self.tour = get_object_or_404(Tour, pk=kwargs["pk"]) #из URL берем параметр pk -> ищем tour с таким id -> если не находим - err 404
        return super().dispatch(request, *args, **kwargs) #передаем управление родительскому классу Django, если GET - вызываем get(), POST - post()

    '''меетод ниже запускается, когда форма прошла валидацию
    (пользователь отправил форму -> Django проверил данные и ошибок нет)'''
    def form_valid(self, form):
        form.instance.tour = self.tour
        form.instance.author = self.request.user
        form.instance.tour_start_date = self.tour.start_date
        form.instance.tour_end_date = self.tour.end_date
        return super().form_valid(form) #сохранение формы в базе данных

    '''метод определяет куда направить пользователя после успешной отправки формы'''
    def get_success_url(self):
        return reverse("tours:detail", kwargs={"pk": self.tour.pk})

    """reverse() - функция Django, которая создает URL по имени маршрута
    tours:detail - имя маршрута из urls.py
    kwargs - параметры url, которые нужно подставить
    self.tour.pk - объект тура, который мы получили в dispatch 
    """