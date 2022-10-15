from django.urls import path
from . import views


urlpatterns = [
    path('', views.restaurant, name='index'),
    path("about_us/", views.about_us, name="about_us"),
    path('basket/', views.BasketView.as_view(), name='basket'),
    path('menu/', views.ViewMenu.as_view(), name='menu'),
    path('order_and_reservation/', views.ViewOrderAndReservation.as_view(), name='order_and_reservation'),
    path('book_reservation/', views.ReservationView.as_view(), name='book_reservation'),
    path('personal_details/', views.PersonalDetailsView.as_view(), name='personal_details'),
]
