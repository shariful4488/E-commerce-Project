from django.urls import path
from product import views


urlpatterns = [
    path('',views.CategoryList.as_view(),name='category-list'),
    path('<int:pk>/', views.ViewSpecificCategory.as_view(), name='view-specific-category')
]
