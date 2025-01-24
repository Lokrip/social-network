from django.views.generic import View
from django.forms import ValidationError
from django.contrib.auth import (
    login,
    logout
)
from django.contrib import messages
from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404
)

from database.models import (
    User,
    Post,
    Friendship,
    MyFriendshipProxy,
    GenerateCodeConfirmationEmail,
)

from .forms import (
    LoginForm,
    SignUpForm,
    EmailConfirmationForm,
)

from home.forms import PostCreateForm

class SettingsView(View):
    def get(self, request):
        return render(request, 'account/settings.html')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        form = LoginForm()
        context = {'title': 'Login', 'form': form}
        return render(request, 'account/login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        form = LoginForm(data=request.POST, request=request)
        
        if form.is_valid():
            try:
                REDIRECT = form.login()    
                messages.success(request, 'Вы успешно вошли в систему!')
                
                return REDIRECT
            except ValidationError as e:
                messages.error(request, e.message)
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
        
        context = {'title': 'Login', 'form': form}
        return render(request, 'account/login.html', context)
    
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        form = SignUpForm()
        context = {'form': form, 'title': 'Регистрация'}
        return render(request, 'account/register.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        form = SignUpForm(request.POST, request=request)
        
        if form.is_valid():
            try:
                user = form.save()
                return form.auth(user)
            except ValidationError as VE:
                raise VE
        
        context = {'form': form, 'title': 'Ошибка'}
        return render(request, 'account/register.html', context)
      
class ConfirmEmail(View):
    def get(self, request, uuid_code):
        if request.user.is_authenticated:
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        
        form = EmailConfirmationForm()
        
        context = {
            'title': 'Подтверждение',
            'form': form
        }
        return render(request, 'account/email/confirm-email.html', context)
    
    def post(self, request, uuid_code):
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            
            try:
                confirm_data = GenerateCodeConfirmationEmail.objects.get(
                    code=code,
                    uuid=uuid_code
                )
                
                confirm_data.user.is_active = True
                confirm_data.user.save()
                
                login(request, confirm_data.user)
                
                confirm_data.delete()
                
                return redirect('social-home:home')
            except GenerateCodeConfirmationEmail.DoesNotExist:
                messages.error(request, "Неверный код подтверждения.")
                   
def logout_user(request):
    logout(request)
    return redirect('account:login')

class ProfileView(View):
    def get(self, request, username):
        user_profile = get_object_or_404(User, username=username)
        friendships_send = Friendship.objects.filter(
            from_user=user_profile,
            to_user=request.user,
            status=Friendship.Status.REQUESTED
        ).first
        
        user_friendships_receive_exists = Friendship.objects.filter(
            to_user=user_profile
        ).exists()
        
        friends = MyFriendshipProxy.objects.all()
        print(friends)
        # posts = Post.objects.prefetch_related(
        #     "product_video",
        #     "product_images"
        # ).filter(user=user_profile)
        
        
        form = PostCreateForm()
        
        context = {
            'title': username,
            "user_profile": user_profile,
            "friendships_send": friendships_send,
            "user_friendships_receive_exists": user_friendships_receive_exists,
            "form": form,
            # "posts": posts
        }
        return render(request, "account/profile.html", context)

