from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from core import views as core_views

api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register(r"schools", core_views.SchoolViewSet)
api_router.register(r"courses", core_views.CourseViewSet)
api_router.register(r"enrollments", core_views.EnrollmentViewSet)
# entities
api_router.register(r"administrators", core_views.AdministratorViewSet)
api_router.register(r"teachers", core_views.TeacherViewSet)
api_router.register(r"students", core_views.StudentViewSet)

# api_router.register(r"schools/<int:pk>/stats/", core_views.SchoolView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/schools/<int:pk>/',
        core_views.SchoolDetails.as_view(),
        name='school-detail'),
    path('api/schools/<int:pk>/stats',
        core_views.SchoolStats.as_view(),
        name='school-stats'),
    path('api/transfer', core_views.transfer_student)
]
