"""mebsuta-django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from mebsuta_api import views
from django.shortcuts import redirect


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cell_images', views.Cell_ImageViewSet)
router.register(r'mebsuta_users', views.Mebsuta_UsersViewSet)
router.register(r'all_annotations', views.AnnotationsViewSet)
router.register(r'cells_annotations', views.CellsAnnotations,
                basename="Annotation")
router.register(r'debris', views.DebrisViewSet)
router.register(r'lib_roll_up', views.LibraryViewSet, basename="Library")
router.register(r'cells', views.MasterCellsViewSet, basename="Cell_Image")
router.register(r'cell_data', views.CellDataViewSet, basename="Cell_Image")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('mebsuta-staging/db-django/api/', include(router.urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', lambda request: redirect('api/', permanent=False)),

]
