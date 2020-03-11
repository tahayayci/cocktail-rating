from django.urls import path

from . import views
from .views import RateView

urlpatterns = [
    path('reviews/<cocktail>/', views.review, name='review'),
    path('rate/<cocktail>/', RateView.as_view(), name='rate'),
    path('add-cocktail/', views.add_cocktail, name='add-cocktail'),
    path('edit-cocktail/<cocktail>/', views.edit_cocktail, name='edit-cocktail'),
    path('delete-cocktail/<cocktail>/', views.delete_cocktail, name='delete-cocktail'),
]
