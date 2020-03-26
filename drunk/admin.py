from django.contrib import admin
from drunk.models import Cocktail, CocktailGroup, CocktailReview, User


class CocktailAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'group_name',
        'is_alcoholic',
        'is_active'
    )

    def group_name(self, obj):
        return obj.group.name


admin.site.register(User)
admin.site.register(Cocktail, CocktailAdmin)
admin.site.register(CocktailGroup)
admin.site.register(CocktailReview)
