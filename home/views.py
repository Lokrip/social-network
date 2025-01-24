import random

from typing import Any

from django.views.generic import (
    TemplateView
)
from django.shortcuts import render

from database.models import (
    Story,
)

from .forms import PostCreateForm

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        
        context['storys'] = Story.objects.select_related('user').order_by('-created_at')
        context['title'] = 'Главная'
        context['form'] = PostCreateForm()
        # #range(1, 4) — это диапазон чисел от 1 до 3 (включая 1 и 3).
        # #random.sample(range(1, 4), 2) выбирает 2 уникальных числа из этого диапазона (1, 2, 3).
        # random_numbers = random.sample(range(15, 35), 2)
        
        # context['random_number_one'], context['random_number_two'] = random_numbers
        return context

    def post(self, request):
        
        context = self.get_context_data()
        return render(request, self.template_name, context)