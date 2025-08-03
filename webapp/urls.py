from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import sitemap_view, robots_txt, ajax_search

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/category/<str:category>/', views.products_by_done, name='products_by_category'),  # фильтр по категории
    path('products/<slug:slug>/', views.item_detail, name='item_detail'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('single-services/', views.single_services, name='single-services'),
    path('item/<slug:slug>/', views.item_details, name='item_details'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('advertisement/', views.advertisement, name='advertisement'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('sitemap.xml', sitemap_view, name='sitemap'),
    path('ajax/search/', ajax_search, name='ajax_search'),

]

# Добавляем маршруты для медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
