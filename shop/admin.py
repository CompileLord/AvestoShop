from django.contrib import admin
from .models import Shop, Category, Post, Cart, Like, Comment, City


class PostInline(admin.TabularInline):
    model = Post
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'bio')
    autocomplete_fields = ('city',)
    inlines = [PostInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'category', 'date_posted')
    list_filter = ('category', 'shop')
    search_fields = ('title', 'content')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

