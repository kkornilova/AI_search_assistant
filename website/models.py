from django.db import models

# Create your models here.


class MealType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CuisineType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DietType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class IntoleranceType(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class UserSavedRecipeLink(models.Model):
    user_id = models.CharField(max_length=None, blank=False, null=False)
    recipe_id = models.CharField(max_length=None, blank=False, null=False)
