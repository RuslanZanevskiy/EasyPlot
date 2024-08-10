from typing import Any, Iterable, List 

import math

from django.contrib.auth.decorators import login_required 
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView
)

from .models import Plot, Like



def rowify_plots(plots: List | QuerySet, rows=3) -> Iterable:
    rowed_plots = []
    index = 0
    for _ in range(math.ceil(len(plots)//rows)+1):
        rowed_plots.append(plots[index:index+rows])
        index += rows  

    return rowed_plots


class PlotListView(ListView):
    model = Plot
    template_name = 'plots/list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = rowify_plots(self.get_queryset()) 
        return context



class PlotDetailView(DetailView):
    model = Plot
    template_name = 'plots/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            if self.request.user is None:
                print(1)
                raise ObjectDoesNotExist
            _ = Like.objects.get(user=self.request.user, plot=self.object)
            print(2)
        except ObjectDoesNotExist:
            context['my_favorite'] = False
        else:
            context['my_favorite'] = True 

        return context

    
class PlotDeleteView(LoginRequiredMixin, DeleteView):
    model = Plot
    success_url = reverse_lazy('plots:list')

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)
    
    def dispatch(self, request: HttpRequest,
                 *args: Any, **kwargs: Any) -> HttpResponseBase:
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
                 *args: Any, **kwargs: Any) -> HttpResponseBase:
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

class PlotMyPlots(LoginRequiredMixin, ListView):
    model = Plot
    template_name = 'plots/myplots.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Plot.objects.filter(author=self.request.user)
        context['object_list'] = rowify_plots(qs) 
        return context

@login_required
def plot_like(request: HttpRequest, pk: int) -> HttpResponse:
    plot = get_object_or_404(Plot, pk=pk) 
    new_like = Like.objects.create(user=request.user, plot=plot)
    new_like.save()
    return redirect('plots:detail', pk=pk) 


@login_required
def plot_unlike(request: HttpRequest, pk: int) -> HttpResponse:
    plot = get_object_or_404(Plot, pk=pk) 
    Like.objects.filter(user=request.user, plot=plot).delete()
    return redirect('plots:detail', pk=pk) 


class PlotLikedView(LoginRequiredMixin, ListView):
    model = Like
    template_name = 'plots/liked.html'
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plots = []
        likes = list(self.get_queryset())
        for like in likes:
            plots.append(like.plot) 

        context['object_list'] = rowify_plots(plots)
        return context
