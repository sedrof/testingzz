
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('addminz/', admin.site.urls),
    path('',include('sellers.urls')),
    path('imports/',include('imports.urls')),
    path('support/',include('support_ticket.urls')),
    path('payout/',include('payout.urls')),
    path('cards/',include('cards.urls')),
    path('orders/',include('orders.urls')),
    path('wallet/',include('wallet.urls')),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
