from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login/', LoginView.as_view(template_name= 'polls/login.html'), name= 'login'),
    path('logout/', LogoutView.as_view(template_name= 'polls/logout.html'), name= 'logout'),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile" ),
    path('edit/', views.edit, name = 'edit'),
    path('pw_change/', views.pw_change, name = 'pw_change'),
]
