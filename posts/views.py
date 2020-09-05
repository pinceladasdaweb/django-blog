from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from comments.models import Comment
from django.contrib import messages


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
    model = Post
    template_name = 'posts/single.html'
    form_class = FormComment
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'post'

    def form_valid(seld, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.comment = post

        if self.request.user.is_authenticated:
            comment.author = self.request.user

        comment.save()
        messages.success(self.request, 'Comment sent successfully.')
        return redirect('post_single', id=post.id)
