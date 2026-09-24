from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Steel Horse Group Admin"
admin.site.site_title = "Steel Horse Group"
admin.site.index_title = "Website & Dispatch"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
