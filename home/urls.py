"""
All URLs for this application 
are stored here
"""
from django.urls import path

from rest_framework.routers import DefaultRouter

from home.api.post_api import (
    PostListApi,
    CreatePostView,
)

from home.api.story_api import (
    CreateStoryView,
    StoryApi
)

from . import views


""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element
"""
app_name = 'home'


# router = DefaultRouter()
# router.register(r"post", CreatePostView, basename='post')

api_post_urlpatterns = [
    path('api/v1/create-post/', CreatePostView.as_view({'post': 'create'})),
    path('api/v1/posts/', PostListApi.as_view()),
    
]

api_story_urlpatterns = [
    path("api/v1/create-story/", CreateStoryView.as_view({'post': 'create'})),
    path("api/v1/story/<str:pk>/", StoryApi.as_view({"get": "retrieve"}))
]

api_urlpatterns = [] + [
    *api_post_urlpatterns,
    *api_story_urlpatterns
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('api/v1/', include(router.urls)),
] + api_urlpatterns
