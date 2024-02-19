from django.urls import path
from product import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.index),
    path('filter/<category_value>', views.filter_by_category),
    path('sorted/<sort_value>', views.sort_by_price),
    path('rating/<rating_value>', views.sort_by_rating),
    path('price', views.filter_by_price_range),
    path('details/<pid>', views.product_detail),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cartview/',views.view_cart),
    path('remove_item/<cartid>',views.remove_item),
    path('update_quantity/<flag>/<cartid>', views.update_quantity),
    path('place_order/', views.place_order),
    # path('make_payment/', views.make_payment),

    
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)