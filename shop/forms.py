from django import forms
from .models import Shop, Category, Post, Like, Comment, City, Cart, PostImage

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title', 'bio', 'city']

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PostForm(forms.ModelForm):
    multiple_images = MultipleFileField(
        label='Additional Images',
        required=False
    )

    class Meta:
        model = Post
        fields = ['category', 'title', 'image', 'description', 'price', 'quantity', 'discount', 'state_product']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['title']


