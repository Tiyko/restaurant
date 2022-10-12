from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Menu, Items, Reservation, User, Orders, Customer, Address
from .forms import CommentForm, ReservationForm, OrderForm


def restaurant(request):
    return render(request, 'index.html')


# def menu(request):
#     return render(request, 'menu.html')

def about_us(request):
    return render(request, 'about_us.html')


class ViewMenu(View):
    model = Menu
    item_model = Items

    def get_user(self, request):
        user_instance = ReservationView().get_user(request)
        return user_instance

    def get_address(self, user_instance_id):         
        try:
            address_instance = Address.objects.get(username_id=user_instance_id)
            return address_instance            
        except Exception as error:
            print('Caught this error: ' + repr(error))

    def get_customer(self, user_instance_id):
        try:
            customer_instance = Customer.objects.get(user_id=user_instance_id)
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
        # seek if 404 or filter     
        order_instance = Orders.objects.filter(id=order_id).first()
        x = self.create_update_order(customer_instance, items_total, order_instance)
        return x

    def post(self, request):
        user_instance = self.get_user(request)
        if user_instance is not None:
            address_instance = self.get_address(user_instance.id)
            customer_instance = self.get_customer(user_instance.id)
            if customer_instance is None:
                customer_instance = self.create_customer(user_instance, address_instance)
                customer_instance.save()

            # get the user infomation the form 
            user_information_from_the_form = request.POST
            quantity = user_information_from_the_form.get('quantity')
            menu_id = user_information_from_the_form.get('menu_id')
            # todo include validation as required on the form because 0 *anything = 0 and just receive numbers maybe type number
            menu_instance = Menu.objects.get(id=menu_id)
            
            items_total = Items().get_total(int(quantity), menu_instance.price)
            # todo create a mechanism to keep the order_id  to add new items in the form, for now not available, change model to have order_opened
            order_id = 0
            # order_instance = self.create_update_order(customer_instance, items_total)
            order_instance = self.get_order(order_id, customer_instance, items_total)     

            items_instance = Items( 
                price=menu_instance.price,
                id_menu=menu_instance,
                order=order_instance,
                quantity=quantity
            )
            items_instance.save()

            message = 'Thank you for your order number ' + str(order_instance.id)

            return redirect('/order_and_reservation/?message=' + message)
        else:
            return render(request, "account/login.html")

        # Should get the id from the selected menu item (menu.id), considering the request.POST object as the information's owner from the html form, with this id should get from database using the menu model and instatiate a Menu object to put it into in items after.

    def get(self, request):
        context = {
            'menu_items': self.model.objects.all(),
            'order_items': self.item_model.objects.all(),
        }
        return render(request, "menu.html", context)


class ViewOrderAndReservation(View):
    items_order = Items
    reservation_model = Reservation

    def post(self, request):
        return render(request, "order_and_reservation.html", context)

    def get(self, request):
        order_message = request.GET.get('message')
        if order_message is None:
            order_message = ''
        reservations_from_user = self.reservation_model.objects.filter(username=request.user.id)
        items_from_user = None
        customer_instance = Customer.objects.filter(user=request.user.id).first()
        if customer_instance is not None:
            order_instance = Orders.objects.filter(customer=customer_instance)
            if order_instance is not None:
                items_from_user = self.items_order.objects.filter(order__in=order_instance)

        context = {
            'orders_items': items_from_user,
            'reservations_items': reservations_from_user,
            'message': order_message
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
            return HttpResponseRedirect('/order_and_reservation/?message=' + 'Thank you for your reservation')
        except Exception as error:
            print('Caught this error: ' + repr(error))


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
