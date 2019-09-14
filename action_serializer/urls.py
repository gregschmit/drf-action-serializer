from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .sample_group_viewset import GroupViewSet


router = DefaultRouter()
router.register("auth/group", GroupViewSet)
router.register("auth/groups", GroupViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
