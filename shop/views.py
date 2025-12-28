from django.views.generic import RedirectView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.db.models import Max, Min, Q, Sum, Avg, Count, F
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from .models import Shop, Category, Post, Cart, Like, Comment, PostImage, Sale, City
from .forms import ShopForm, PostForm, CityForm, CommentForm, LikeForm, CartForm

# Create your views here.

class MainListView(ListView):
    model = Category
    template_name = 'main.html'
    context_object_name = 'categories'
    def get_queryset(self):
        return Category.objects.prefetch_related('posts').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_products'] = Post.objects.filter(discount__gt=0).annotate(
            like_count=Count('like')
        ).order_by('-like_count', '-discount')[:3]

        queryset = Post.objects.all()
        
        status = self.request.GET.get('status')
        sort = self.request.GET.get('sort')
        category = self.request.GET.get('category')
        city = self.request.GET.get('city')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if city:
            queryset = queryset.filter(shop__city_id=city)
        
        if status:
            queryset = queryset.filter(state_product=status)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-date_posted')
        
        context['posts'] = queryset
        context['cities'] = City.objects.all()
        return context

class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'posts'
    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        sort = self.request.GET.get('sort')
        city = self.request.GET.get('city')
        category = self.request.GET.get('category')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if city:
            queryset = queryset.filter(shop__city_id=city)
        
        if status:
            queryset = queryset.filter(state_product=status)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                context['selected_category'] = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                context['selected_category'] = None
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        context['cities'] = City.objects.all()
        return context

class ShopDetailView(DetailView):
    model = Shop
    template_name = 'shop_detail.html'
    context_object_name = 'shop'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Post.objects.filter(shop=self.object)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_post = self.object

        context['recomendation'] = Post.objects.filter(
            category=curr_post.category
            ).exclude(pk=curr_post.pk)[:4]
        context['comments'] = Comment.objects.filter(
            post = curr_post.pk
        )
        context['count_likes'] = Like.objects.filter(post=curr_post.pk).aggregate(Count('id'))
        return context


class ShopDashboardView(LoginRequiredMixin, DetailView):
    model = Shop
    template_name = 'shop_dashboard.html'
    context_object_name = 'shop'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_shop = self.object
        context['last_posts'] = Post.objects.filter(shop=curr_shop).order_by('-date_posted')[:6]
        context['list_comments'] = Comment.objects.filter(post__shop=curr_shop).order_by('-id')[:5]
        context['last_sales'] = Sale.objects.filter(post__shop=curr_shop).order_by('-id')[:5]
        context['count_sales'] = Sale.objects.filter(post__shop=curr_shop).aggregate(Count('id'))
        context['count_likes'] = Like.objects.filter(post__shop=curr_shop).aggregate(Count('id'))
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('main')
    def form_valid(self, form):
        form.instance.shop = Shop.objects.get(user=self.request.user)
        response = super().form_valid(form)
        images = self.request.FILES.getlist('multiple_images')
        for image in images:
            PostImage.objects.create(post=self.object, image=image)
        
        return response

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_images'] = PostImage.objects.filter(post=self.object)
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('multiple_images')
        for image in images:
            PostImage.objects.create(post=self.object, image=image)
        
        return response
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('main')

class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'shop_form.html'
    success_url = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        if Shop.objects.filter(user=request.user).exists():
            shop = Shop.objects.get(user=request.user)
            return redirect('shop_dashboard', pk=shop.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    def form_valid(self, form):
        form.instance.from_user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class LikeCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_obj = Post.objects.get(pk=self.kwargs['post_id'])
        like_qs = Like.objects.filter(from_user=request.user, post=post_obj)
        
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(from_user=request.user, post=post_obj)
            
        return redirect('post_detail', pk=post_obj.pk)

class AddToCartView(LoginRequiredMixin, CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'shop/cart_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['post_id'])
        return context

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        quantity = int(self.request.POST.get('quantity', 1))
        
        if quantity > post.quantity:
            form.add_error('quantity', f"Only {post.quantity} items available.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.post = post
        form.instance.quantity = quantity
        post.quantity -= quantity
        post.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['post_id']})

class DeleteFromCartView(LoginRequiredMixin, DeleteView):
    model = Cart
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cart')

class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart_items'
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cart = Cart.objects.filter(user=self.request.user)
        total_data = user_cart.aggregate(
            total=Sum(F('quantity') * F('post__price'))
        )
        context['total_price'] = total_data['total'] or 0
        return context


class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        try:
            shop = Shop.objects.get(user=self.request.user)
            return reverse('shop_dashboard', kwargs={'pk': shop.pk})
        except Shop.DoesNotExist:
            return reverse('shop_create')

class ConfirmSaleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.exists():
            for item in cart_items:
                Sale.objects.create(
                    customer = request.user,
                    post = item.post,
                    quantity = item.quantity,
                    price = item.post.price,
                    total_price = item.post.price * item.quantity
                )
            cart_items.delete()
            messages.success(request, "All items have been successfully purchased!")
        else:
            messages.error(request, 'Your cart is empty.')
        return redirect('cart')
