from django.urls import path

from . import views
from account.api import user_api


app_name = 'account'


api_urlpatterns = [
    path("api/v1/user-detail/", user_api.UserApi.as_view(), name="user-detail")
]

auth_urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('sign-in/', views.RegisterView.as_view(), name='sign-in'),
    path(
        'confirm-email/code/<uuid:uuid_code>/', 
        views.ConfirmEmail.as_view(),
        name='confirm-email'
    )
]

urlpatterns = [
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/@<username>/', views.ProfileView.as_view(), name='profile'),
    
] + [*auth_urlpatterns, *api_urlpatterns]
