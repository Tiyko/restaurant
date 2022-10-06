from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Menu, Items, Reservation, User, Orders, Customer, Address
from .forms import CommentForm, ReservationForm


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
        if request.user.is_authenticated:  
            user_instance = User.objects.get(id=request.user.id)
            return user_instance
        else:
            return None

    def items_object_example(self):
        user_instance = User(
        
            first_name='sas',
            last_name='dsa',
            email='asd@sd.ocm',
            username='dffff',
            is_superuser=True)
        
        address_instance = Address(
            username=user_instance,
            address='sadas',
            zipcode='sdasdasdas'
        )
        
        customer_instance = Customer(
            user=user_instance,
            address=address_instance
        )
        
        menu_instance = Menu(
            meal_name='pizza',
            meal_description='pissssz',
            price=33
        )
        
        order_instance = Orders(
            total_price='23333',
            customer=customer_instance
        )
        
        items_instance = Items( 
            price='23',
            id_menu=menu_instance,
            order=order_instance,
            quantity=55
        )
        
        user_instance.save()
        address_instance.save()
        customer_instance.save()
        order_instance.save()
        menu_instance.save()
        items_instance.save()
        
        return items_instance

    def post(self, request):

        return render(request, "menu.html", {"blah": "it_worked"})

    def get(self, request):
        context = {
            'menu_items': self.model.objects.all(),
            'order_items': self.item_model.objects.all(),
        }
        return render(request, "menu.html", context)


class ViewOrderAndReservation(View):
    order_model = Items
    reservation_model = Reservation

    def get(self, request):
        context = {
            'orders_items': self.order_model.objects.all(),
            'reservations_items': self.reservation_model.objects.all(),
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
            return HttpResponse('thanks')
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
