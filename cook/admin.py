from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


class RecipeInline(admin.StackedInline):  # интегрируются окна для заполнения рецептов в админке для добавления в пост
    model = models.Recipe
    extra = 1  # вывод одного окна при заполнении, по умолчанию их появляется три


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "create_at", "id"]  # то что выводится в админке
    inlines = [RecipeInline]  # добавляется этот класс в модель с постами


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "prep_time", "cook_time", "post"]  # то что выводится в админке


admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Tag)

admin.site.register(models.Comment)
