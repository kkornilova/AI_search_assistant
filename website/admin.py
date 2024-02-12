from django.contrib import admin
from .models import MealType, CuisineType, DietType, IntoleranceType
# Register your models here.


class MealTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class CuisineTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class DietTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class IntoleranceTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(MealType, MealTypeAdmin)
admin.site.register(CuisineType, CuisineTypeAdmin)
admin.site.register(DietType, DietTypeAdmin)
admin.site.register(IntoleranceType, IntoleranceTypeAdmin)
