from django.urls import path
from . import views
from .views import HomePage, AboutPage, ProfilePage, Jobs, SignupPage, LoginPage , JobDetail

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('home', HomePage.as_view(), name='home'),
    path('about', AboutPage.as_view(), name='about'),
    path('profile', ProfilePage.as_view(), name='profile'),
    path('jobs', Jobs.as_view(), name='jobs'),
    path('contact',views.contact_view, name='contact'),
    path('login', LoginPage.as_view(), name='login'),
    path('login/', LoginPage.as_view(), name='login'),
    path('signup', SignupPage.as_view(), name='signup'),
    path('signup/', SignupPage.as_view(), name='signup'),
    path('job/<int:job_id>/', views.JobDetail.as_view(), name='job_detail'),
    path('apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
]

