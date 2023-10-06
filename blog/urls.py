from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.login_view, name='login'),
    path('blog/ticket_list', views.ticket_list, name='ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
