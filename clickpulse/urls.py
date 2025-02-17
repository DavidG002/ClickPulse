# C:\Users\David\Apps-Start\Start-ClickPulse\clickpulse\urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analytics/', include('analytics.urls')),
    path('', lambda request: redirect('api/analytics/grafana/', permanent=True)),
]