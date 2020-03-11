from django.contrib import admin
from drunk.models import Cocktail, CocktailGroup, CocktailReview

admin.site.register(Cocktail)
admin.site.register(CocktailGroup)
admin.site.register(CocktailReview)