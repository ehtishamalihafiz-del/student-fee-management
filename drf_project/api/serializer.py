from rest_framework import serializers
from .models import Student, FeeRecord


class FeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FeeRecord
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    fee_records = FeeRecordSerializer(many=True, read_only=True)
    total_fees  = serializers.SerializerMethodField()
    paid_fees   = serializers.SerializerMethodField()
    pending_fees = serializers.SerializerMethodField()

    class Meta:
        model  = Student
        fields = ['id', 'name', 'roll_number', 'department',
                  'email', 'phone', 'created_at',
                  'fee_records', 'total_fees', 'paid_fees', 'pending_fees']

    def get_total_fees(self, obj):
        return sum(r.amount for r in obj.fee_records.all())

    def get_paid_fees(self, obj):
        return sum(r.amount for r in obj.fee_records.filter(status='paid'))

    def get_pending_fees(self, obj):
        return sum(r.amount for r in obj.fee_records.exclude(status='paid'))