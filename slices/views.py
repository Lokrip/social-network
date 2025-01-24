from django.views.generic import View
from django.shortcuts import render
from django.db.models import Prefetch


from database.models import (
    Post,
    PostVideo
)

class SlicesHome(View): 
    def get(self, request): 
        slices = Post.objects.select_related(
            "user"
        ).prefetch_related(
            "product_video", 
        ).filter(
            product_video__video__isnull=False
        ).order_by("-pk")

        context = {
            'title': 'Slices',
            "slices": slices
        }
        return render(request, 'slices/default-video.html', context)