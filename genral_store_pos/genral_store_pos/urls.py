
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls',)),
    path('inventory/', include('inventory.urls',)),
    path('invoice/', include('pos.urls',)),
]
