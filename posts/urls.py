from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('category/<str:category>', views.PostCategory.as_view(), name='post_category'),
    path('search/', views.PostSearch.as_view(), name='post_search'),
    path('single/<int:id>', views.PostSingle.as_view(), name='post_single'),
]
