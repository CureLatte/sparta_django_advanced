from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from tabom.apis.v1.article_router import router as article_router
from tabom.apis.v1.like_router import router as like_router

api = NinjaAPI()
api.add_router("/likes/", like_router)
api.add_router("/articles/", article_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
