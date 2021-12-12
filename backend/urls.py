from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

# Configuration des medias 
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('accounts.endpoints')),

    path('schema/', get_schema_view(
        title="USersAPI",
        description="API for the Users",
        version="1.0.0"
    ), name="users-schema"),
    path('', include_docs_urls(
        title="UserAPI",
        description="API for the Users",
    ), name="users-docs")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)