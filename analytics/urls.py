# analytics/urls.py
from django.urls import path
from .views import (
    total_sales_per_day_view,
    total_sales_by_country_view,
    average_order_value_view,
    grafana_dashboard,
    performance_metric_view,
)

urlpatterns = [
    path('sales-per-day/', total_sales_per_day_view, name='sales_per_day'),
    path('sales-by-country/', total_sales_by_country_view, name='sales_by_country'),
    path('avg-order-value/', average_order_value_view, name='avg_order_value'),
    path('grafana/', grafana_dashboard, name='grafana_dashboard'),
    path('performance/', performance_metric_view, name='performance_metric'),
]