from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_expert = models.BooleanField(default=False)


class CocktailGroup(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ForeignKey(CocktailGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    is_alcoholic = models.BooleanField()
    recipe = models.TextField(max_length=256)
    picture = models.ImageField(upload_to='cocktail_images/')
    is_active = models.BooleanField()

    def __str__(self):
        return self.name


class CocktailReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.PROTECT)
    taste_star = models.PositiveSmallIntegerField()
    cost_star = models.PositiveSmallIntegerField()
    prep_hardness_star = models.PositiveSmallIntegerField()
    notes = models.TextField()
