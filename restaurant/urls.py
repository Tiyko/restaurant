from django.urls import path
from . import views

# from restaurant.views import PostMenu


urlpatterns = [
    path('', views.restaurant, name='index'),
    path("about_us/", views.about_us, name="about_us"),

    path('menu/', views.ViewMenu.as_view(), name='menu'),

    path('', views.PostList.as_view(), name='index'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
