from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, FeeRecordViewSet

router = DefaultRouter()
router.register(r'students',   StudentViewSet,   basename='student')
router.register(r'fee-records', FeeRecordViewSet, basename='feerecord')

urlpatterns = [
    path('', include(router.urls)),
]