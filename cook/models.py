from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# тут используем модуль mptt для построения бинарного дерева, то есть вложенные категории
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/')
    text = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name="post",
        on_delete=models.SET_NULL,
        null=True
    )
    tags = models.ManyToManyField(Tag, related_name="post")
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse("post_single", kwargs={"slug": self.category.slug, "post_slug": self.slug})

    def __str__(self):
        return self.title

    def get_recipes(self):
        return self.recipes.all()


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    serves = models.CharField(max_length=50)
    prep_time = models.PositiveIntegerField(default=0)
    cook_time = models.PositiveIntegerField(default=0)
    ingredients = models.TextField()
    directions = models.TextField()
    post = models.ForeignKey(
        Post,
        related_name="recipes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(max_length=500)

    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
