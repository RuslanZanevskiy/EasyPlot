from typing import Any

from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse

from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)

from .models import Plot


class PlotListView(ListView):
    model = Plot
    template_name = 'plots/list.html'
    paginate_by = 9


class PlotDetailView(DetailView):
    model = Plot
    template_name = 'plots/detail.html'


class PlotDeleteView(LoginRequiredMixin, DeleteView):
    model = Plot
    success_url = reverse_lazy('plots:list')

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)
    
    def dispatch(self, request: HttpRequest, 
                 *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            if self.get_object().author != request.user:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PlotCreateView(LoginRequiredMixin, CreateView):
    model = Plot
    fields = ['title', 'description', 'code', 'main_image']
    template_name = 'plots/form.html'
    extra_context = {'title': 'Create a new Plot'}
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)


class PlotUpdateView(LoginRequiredMixin, UpdateView):
    model = Plot
    fields = ['title', 'description', 'code', 'main_image']
    template_name = 'plots/form.html'
    extra_context = {'title': 'Create a new Plot'}

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)

    def dispatch(self, request: HttpRequest,
                 *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            if self.get_object().author != request.user:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PlotSignupView(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserCreationForm


class PlotUpdateUserView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/update_user.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('plots:list')
    model = User


class PlotProfileView(ListView):
    pass

class PlotLikedView(ListView):
    pass
