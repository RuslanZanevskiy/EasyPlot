from typing import Any

import math

from django.http import Http404
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


class PlotProfileView(LoginRequiredMixin, DetailView):
    template_name = 'registration/profile.html'
    model = User

    def get_queryset(self):
        qs = super(PlotProfileView, self).get_queryset()
        return qs.filter(pk=self.request.user.pk)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                ("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plots = Plot.objects.filter(author=self.object)
        n = 3
        rows = []
        index = 0
        for i in range(math.ceil(len(plots)//n)+1):
            rows.append(plots[index:index+n])
            index += n

        context['my_plots'] = rows
        return context


class PlotLikedView(ListView):
    pass
    #TODO
