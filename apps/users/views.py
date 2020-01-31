from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, ProfilForm
from .models import CustomUser


class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        temp = super().get_context_data(**kwargs)
        tem = temp
        return tem


class ProfilView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfilForm
    success_url = reverse_lazy('profil')
    template_name = 'users/profil.html'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(pk=self.request.user.id)
