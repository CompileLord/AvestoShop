from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm

# Create your views here.
class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')