from django.db import models

class Student(models.Model):
    name        = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    department  = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone       = models.CharField(max_length=15)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class FeeRecord(models.Model):
    STATUS_CHOICES = [
        ('paid',    'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ]
    FEE_TYPE_CHOICES = [
        ('tuition',      'Tuition Fee'),
        ('examination',  'Examination Fee'),
        ('library',      'Library Fee'),
        ('hostel',       'Hostel Fee'),
        ('transport',    'Transport Fee'),
    ]

    student      = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    fee_type     = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount       = models.DecimalField(max_digits=10, decimal_places=2)
    due_date     = models.DateField()
    paid_date    = models.DateField(null=True, blank=True)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    semester     = models.CharField(max_length=20)
    remarks      = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.fee_type} - {self.status}"