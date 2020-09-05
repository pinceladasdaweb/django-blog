from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-id').filter(published=True)
        qs = qs.annotate(
            count_comments = Count(
                Case(
                    When(
                        comment__published=True, then=1
                    )
                )
            )
        )

        return qs


class PostSearch(PostIndex):
    template_name = 'posts/search.html'

    def get_queryset(self):
        qs = super().get_queryset()

        term = self.request.GET.get('term', None)

        if not term:
            return qs

        qs = qs.filter(
            Q(author__first_name__iexact=term) |
            Q(title__icontains=term) |
            Q(content__icontains=term) |
            Q(excerpt__icontains=term) |
            Q(category__cat_name__iexact=term)
        )

        return qs


class PostCategory(PostIndex):
    template_name = 'posts/category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.kwargs.get('category', None)

        if not category:
            return qs

        qs = qs.filter(category__cat_name__iexact=category)

        return qs


class PostSingle(UpdateView):
    pass
