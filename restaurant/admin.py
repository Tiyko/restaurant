from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Reservation, Address, Orders, Menu, Items


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'reservation_date', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'address', 'zipcode', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'total_price', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    list_display = ['id', 'meal_name', 'meal_description', 'price', 'imageUrl', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):

    list_display = ['id', 'meal_name', 'menu_id', 'order_id', 'quantity', 'price_menu', 'created_on']
    search_fields = ['id']
    list_filter = ['created_on']

    def meal_name(self, obj):
        return obj.id_menu.meal_name

    def menu_id(self, obj):
        return obj.id_menu.id

    def order_id(self, obj):
        return obj.order.id

    def price_menu(self, obj):
        return obj.id_menu.price
