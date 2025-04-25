
from product.models import Product,Category,Review,ProductImage
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema



# Create your views here.D


    
class ProductViewSet(ModelViewSet):
    """
    Product viewset that provides standard actions
     ~ Allows authenticated users to create, update, and delete products
        ~ Allows all users to view products
    ~ Allows admin users to view, create, update, and delete products

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    search_fields = ['name','description']
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]



    @swagger_auto_schema(
            operation_summary='Retrieve a list of products'
    )
    def list(self, request, *args, **kwargs):
        """
        only admin users can view all products
        """

        return super().list(request, *args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary = "Create a product",
        operation_description="This allows admin users to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        """
        only admin users can create products
        """
        return super().create(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))





    
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

     
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))


    def get_serializer_coontext(self):
        return {'product_id':self.kwargs.get('product_pk')}

