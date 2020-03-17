from django.contrib import admin
from drunk.models import Cocktail, CocktailGroup, CocktailReview, User

admin.site.register(User)
admin.site.register(Cocktail)
admin.site.register(CocktailGroup)
admin.site.register(CocktailReview)
