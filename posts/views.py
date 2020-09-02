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
    pass


class PostCategory(PostIndex):
    pass


class PostSingle(UpdateView):
    pass
