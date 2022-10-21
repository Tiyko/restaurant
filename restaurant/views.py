from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from .models import Menu, Items, Reservation, User, Orders, Customer, Address
from .forms import ReservationForm


def restaurant(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about_us.html')


class PersonalDetailsView(View):

    def get(self, request):
        user_instance = User.objects.get(id=request.user.id)
        if user_instance is not None:
            address_instance = Address.objects.filter(username=user_instance).first()

        context = {
            'first_name': user_instance.first_name,
            'last_name': user_instance.last_name,
            'email': user_instance.email,
            'address': '' if address_instance is None else address_instance.address,
            'zipcode': '' if address_instance is None else address_instance.zipcode
        }
        return render(request, "personal_details.html", context)

    def post(self, request):
        user_instance = User.objects.get(id=request.user.id)
        if user_instance is not None:
            address_instance = Address(
                username=user_instance,
                address=request.POST.get('address'),
                zipcode=request.POST.get('zipcode')
            )
            address_instance.save()

            user_instance.email = request.POST.get('email')
            user_instance.first_name = request.POST.get('first_name')
            user_instance.last_name = request.POST.get('last_name')
            user_instance.save()
        return redirect('/menu', request)


class ViewMenu(View):
    model = Menu
    item_model = Items

    def get_user(self, request):
        user_instance = ReservationView().get_user(request)
        return user_instance

    def get_address(self, user_instance_id):
        try:
            address_instance = Address.objects.filter(username_id=user_instance_id).first()
            return address_instance
        except Exception as error:
            print('Caught this error: ' + repr(error))

    def get_customer(self, user_instance_id):
        try:
            customer_instance = Customer.objects.filter(user_id=user_instance_id).first()
            return customer_instance

        except Exception as error:    
            print('Caught this error: ' + repr(error))

    def create_customer(self, user_instance, address_instance):
        customer_instance = Customer(
            user=user_instance,
            address=address_instance
        )
        return customer_instance

    def create_update_order(self, customer_instance, items_total, order_instance):
        if order_instance is None:
            order_instance = Orders(
                total_price=self.calculate_total_price(0, items_total),
                customer=customer_instance
                ) 
            order_instance.save()
            return order_instance
        order_instance_update = order_instance
        order_instance_update.total_price = self.calculate_total_price(order_instance.total_price, items_total)
        order_instance_update.save()
        return order_instance_update

    def calculate_total_price(self, old_order_price, items_total):
        totalprice = old_order_price + items_total
        return totalprice 

    def get_order(self, order_id, customer_instance, items_total):
        order_instance = Orders.objects.filter(id=order_id).first()
        return self.create_update_order(customer_instance, items_total, order_instance)

    def post(self, request):
        user_instance = self.get_user(request)
        if user_instance is not None:
            address_instance = self.get_address(user_instance.id)
            if address_instance is None:
                return redirect('/personal_details', request)

            customer_instance = self.get_customer(user_instance.id)
            if customer_instance is None:
                customer_instance = self.create_customer(user_instance, address_instance)
                customer_instance.save()

            user_information_from_the_form = request.POST
            quantity = user_information_from_the_form.get('quantity')
            menu_id = user_information_from_the_form.get('menu_id')
            menu_instance = Menu.objects.get(id=menu_id)
            items_total = Items().get_total(int(quantity), menu_instance.price)
            order_id = request.POST.get('order_from_basket')
            order_instance = self.get_order(order_id, customer_instance, items_total)     

            items_instance = Items( 
                price=menu_instance.price,
                id_menu=menu_instance,
                order=order_instance,
                quantity=quantity
            )
            items_instance.save()

            message = 'Your item was added '
            return redirect('/basket/?message=' + message)
        else:
            return render(request, "account/login.html")

    def get(self, request):
        order_from_basket = 0
        if request.session.get('order_from_basket', False):    
            order_from_basket = request.session['order_from_basket']
        context = {
            'menu_items': self.model.objects.all(),
            'order_items': self.item_model.objects.all(),
            'order_from_basket': order_from_basket
        }
        return render(request, "menu.html", context)


class ViewOrderAndReservation(View):
    items_order = Items
    reservation_model = Reservation

    def post(self, request):

        if request.POST.get('delete_order') is not None:
            order_instance = Orders.objects.get(id=request.POST.get('delete_order'))
            order_instance.delete()
        elif request.POST.get('delete_reservation') is not None:
            reservation_instance = Reservation.objects.get(id=request.POST.get('delete_reservation'))
            reservation_instance.delete()
        return redirect('/order_and_reservation', request)

    def get(self, request):
        order_message = request.GET.get('message')
        if order_message is None:
            order_message = ''
        reservations_from_user = self.reservation_model.objects.filter(username=request.user.id)
        items_from_user = None
        customer_instance = Customer.objects.filter(user=request.user.id).first()
        order_instance = None
        if customer_instance is not None:
            order_instance = Orders.objects.filter(customer=customer_instance)
            if order_instance is not None:
                items_from_user = self.items_order.objects.filter(order__in=order_instance)

        context = {
            'orders_items': '' if items_from_user is None else items_from_user,
            'reservations_items': '' if reservations_from_user is None else reservations_from_user,
            'message': order_message,
            'orders': '' if order_instance is None else order_instance
        }

        return render(request, "order_and_reservation.html", context)


class ReservationView(View):

    def get_user(self, request):
        if request.user.is_authenticated:  
            user_instance = User.objects.get(id=request.user.id)
            return user_instance
        else:
            return None

    def save_reservation(self, request):
        try:
            object_reservation_form = ReservationForm(data=request.POST)
            form_info = object_reservation_form.data.dict()

            user_instance = self.get_user(request)

            reservation_instance = Reservation(
                username=user_instance,
                number_of_people=form_info.get("number_of_people"),
                reservation_date=form_info.get("date"),
                reservation_time=form_info.get("time"))
            reservation_instance.save()

        except Exception as error:
            print('Caught this error: ' + repr(error))

    def get(self, request):
        user_instance = self.get_user(request)
        if user_instance is not None:
            context = {
                        'first_name': user_instance.first_name,
                        'last_name': user_instance.last_name,
                        'email': user_instance.email,
                    }
            return render(request, "book_reservation.html", context)
        else:
            return render(request, "account/login.html")

    def post(self, request):
        try:
            self.save_reservation(request)
            message = 'Thank you for your reservation'
            return HttpResponseRedirect('/order_and_reservation/?message=' + message)
        except Exception as error:
            print('Caught this error: ' + repr(error))


class BasketView(View):
    def calculate_remained_total_price(self,total_order_price, total_items_price):
        remained_total = total_order_price - total_items_price
        return remained_total

    def post(self, request):
    
        if request.POST.get('pay') == 'pay':
            order_instance = Orders.objects.get(id=request.POST.get('order_id'))
            order_instance.paid = True
            order_instance.save()
            request.session['order_from_basket'] = None
            message = 'Thank you for your order!'
            return HttpResponseRedirect('/order_and_reservation/?message=' + message)

        elif request.POST.get('add_more_items') == 'add_more_items':
            request.session['order_from_basket'] = request.POST.get('order_id')
            return redirect('/menu', request)

        elif request.POST.get('remove_item') is not None:
            item_id = request.POST.get('remove_item')
            item_instance = Items.objects.get(id=item_id)

            order_instance = Orders.objects.get(id=request.POST.get('order_id'))   
            total_items_price  = Items().get_total(item_instance.quantity, item_instance.price)
            order_instance.total_price = self.calculate_remained_total_price(order_instance.total_price, total_items_price)

            order_instance.save()
            item_instance.delete()
            return redirect('/basket', request)

    def get(self, request):
        order_instance = None
        order_message = request.GET.get('message')
        if order_message is None:
            order_message = ''
        items_from_user = None
        customer_instance = Customer.objects.filter(user=request.user.id).first()
        if customer_instance is not None:
            order_instance = Orders.objects.filter(customer=customer_instance).filter(paid=False).last()
            if order_instance is not None:
                items_from_user = Items.objects.filter(order=order_instance)

        context = {
            'orders_items': items_from_user,
            'message': order_message,
            'order_id': 0 if order_instance is None else order_instance.id,
            'total_price': None if order_instance is None else order_instance.total_price
        }

        return render(request, "basket.html", context)
