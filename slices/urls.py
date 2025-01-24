"""
All URLs for this application 
are stored here
"""
from django.urls import path
from . import views


""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element
"""
app_name = 'slices'

urlpatterns = [
    path('', views.SlicesHome.as_view(), name='home'),
]
