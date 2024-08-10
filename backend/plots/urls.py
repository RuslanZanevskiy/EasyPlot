from django.urls import path

from .views import (
    PlotListView,
    PlotDetailView,
    PlotCreateView,
    PlotDeleteView,
    PlotUpdateView,
    PlotSignupView,
    PlotProfileView,
    PlotUpdateUserView,
    PlotMyPlots,

    PlotLikedView,
    plot_like,
    plot_unlike,
)


app_name = 'plots'

urlpatterns = [
    path('', PlotListView.as_view(), name='list'), 
    path('<int:pk>', PlotDetailView.as_view(), name='detail'), 
    path('<int:pk>/delete', PlotDeleteView.as_view(), name='delete'), 
    path('<int:pk>/update', PlotUpdateView.as_view(), name='update'), 
    path('new', PlotCreateView.as_view(), name='create'), 

    path('signup', PlotSignupView.as_view(), name='signup'),
    path('update_info', PlotUpdateUserView.as_view(), name='update_user'),

    path('profile', PlotProfileView.as_view(), name='profile'),
    path('myplots', PlotMyPlots.as_view(), name='myplots'),

    path('<int:pk>/like', plot_like, name='like'),
    path('<int:pk>/unlike', plot_unlike, name='unlike'),
    path('liked', PlotLikedView.as_view(), name='liked'),
]
