# urls.py
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import MyAPI, paypal_payment_view

router = routers.DefaultRouter()
router.register(r'backend-api', MyAPI)

schema_view = get_schema_view(
    openapi.Info(
        title="Backend Django API",
        default_version='v1',
        description="Api Rest em Python com Django integrado com Swagger e Paypal",
        contact=openapi.Contact(email="emerson_tecno@hotmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('paypal/', paypal_payment_view, name='paypal'),
]
