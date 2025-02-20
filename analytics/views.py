# C:\Users\David\Apps-Start\Start-ClickPulse\analytics\views.py
from django.http import JsonResponse
from .clickhouse_queries import measure_total_sales_query_time
from django.shortcuts import render, redirect
from django.conf import settings
from .clickhouse_queries import (
    get_total_sales_per_day,
    get_total_sales_by_country,
    get_average_order_value,
)

def total_sales_per_day_view(request):
    data = get_total_sales_per_day()
    return JsonResponse(data, safe=False)

def total_sales_by_country_view(request):
    data = get_total_sales_by_country()
    return JsonResponse(data, safe=False)

def average_order_value_view(request):
    avg_value = get_average_order_value()
    return JsonResponse({"average_order_value": avg_value})

def performance_metric_view(request):
    execution_time = measure_total_sales_query_time()
    return JsonResponse({"total_sales_query_time_ms": execution_time})

def grafana_dashboard(request):
    if settings.DEBUG:
        grafana_url = grafana_url = "http://localhost:3000/public-dashboards/f72afd8fdbfd42759197ad85cfa5b1d0"
    else:
        grafana_url = "https://clickpulse.daveedg.com/grafana-dash/public-dashboards/1fb2f63c2b0047df9f517244722a824d"
    return render(request, "analytics/grafana_dashboard.html", {"grafana_url": grafana_url})