from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        temp = super().get_context_data(**kwargs)
        tem = temp
        return tem
