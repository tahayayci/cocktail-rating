from django.contrib import admin
from drunk.models import Cocktail, CocktailGroup, CocktailReview, User


class CocktailAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'group__name',
        'is_alcoholic',
        'is_active'
    )


admin.site.register(User)
admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(CocktailGroup)
admin.site.register(CocktailReview)
