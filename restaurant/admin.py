from django.contrib import admin
from .models import Reservation, Address, Orders, Menu, Items, Customer


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'reservation_date', 'reservation_time', 'number_of_people', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'address', 'zipcode', 'created_on']
    search_fields = ['username', 'id']
    list_filter = ['created_on']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'customer_address']
    search_fields = ['user', 'id']
    list_filter = ['created_on']

    def customer_address(self, obj):
        return obj.address.address


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    list_display = ['id', 'customer', 'total_price', 'created_on']
    search_fields = ['customer', 'id']
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
