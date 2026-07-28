from django.urls import path
from . import views
from .views import StudentList,StudentDetail
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet


urlpatterns = [
    path("",views.home),
    path("name/",views.students,name = "students"),
    path(
        "students/",
        StudentList.as_view()
    ),

    path(
        "students/<int:pk>/",
        StudentDetail.as_view()
    ),
]

router = DefaultRouter()
router.register("students",StudentViewSet)
urlpatterns = router.urls