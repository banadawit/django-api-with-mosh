from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

product_router =  routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
urlpatterns = router.urls + product_router.urls


# URLConf
# urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
# ]
