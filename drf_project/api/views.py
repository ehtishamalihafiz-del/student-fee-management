from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student, FeeRecord
from .serializer import StudentSerializer, FeeRecordSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'roll_number', 'department', 'email']
    ordering_fields  = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def fee_summary(self, request, pk=None):
        student = self.get_object()
        records = student.fee_records.all()
        return Response({
            'student'      : student.name,
            'roll_number'  : student.roll_number,
            'total_fees'   : sum(r.amount for r in records),
            'paid_fees'    : sum(r.amount for r in records.filter(status='paid')),
            'pending_fees' : sum(r.amount for r in records.filter(status='pending')),
            'overdue_fees' : sum(r.amount for r in records.filter(status='overdue')),
            'total_records': records.count(),
        })


class FeeRecordViewSet(viewsets.ModelViewSet):
    queryset         = FeeRecord.objects.all().select_related('student')
    serializer_class = FeeRecordSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'fee_type', 'semester', 'student']
    search_fields    = ['student__name', 'student__roll_number', 'remarks']
    ordering_fields  = ['due_date', 'amount', 'created_at']