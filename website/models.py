from django.db import models

# Create your models here.


class MealType(models.Model):
    name = models.CharField(max_length=50)


class CuisineType(models.Model):
    name = models.CharField(max_length=50)


class DietType(models.Model):
    name = models.CharField(max_length=50)


class IntoleranceType(models.Model):
    name = models.CharField(max_length=70)
