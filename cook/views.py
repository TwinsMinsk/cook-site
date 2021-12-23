from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from cook.models import Post


class PostListView(ListView):
    model = Post

    def get_queryset(self): # переопределяем queryset, фильтруем по слагу, select_related - останавливает запросы к базе данных
        return Post.objects.filter(category__slug=self.kwargs.get("slug")).select_related('category')


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"  # это мы определяем как будет называться нащ объект в шаблоне
    slug_url_kwarg = "post_slug"  # переименуем slug для вывода в url



def home(request):
    return render(request, 'base.html')