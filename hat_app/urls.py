from django.urls import path
from django.conf.urls.static import static  # Add this import

from hat_solutions import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    # Add more URLs for other pages
    # path('portfolio/', views.portfolio, name='portfolio'),
    path('team/', views.team, name='team'),
    # path('contact/', views.contact, name='contact'),
    path('contact/', views.contact_view, name='contact_view'),
    path('success/', views.success_page, name='success_page'),  # Add this line
    # path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/', views.portfolio_list, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    # path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)