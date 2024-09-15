from django.db import models
from django.conf import settings

class Bill(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated field

    def __str__(self):
        return f"{self.title} - {self.amount}"

class BillSplit(models.Model):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='splits'
    )
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='paid_splits'
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    owed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owed_splits'
    )
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")  # pending, paid

    def __str__(self):
        return f"{self.owed_by} owes {self.amount_owed} for {self.bill}"
