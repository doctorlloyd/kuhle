from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import ViewOders, Customers, StatusCode

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('app/', 'static/data.csv'),
    path('api/orders', ViewOders.as_view()),
    path('api/customers', Customers.as_view()),
    path('api/status', StatusCode.as_view()),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)