from rest_framework import serializers
from BillManagement.models import Bill, BillSplit

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'title', 'description', 'amount', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class BillSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillSplit
        fields = ['id', 'bill', 'paid_by', 'amount_paid', 'owed_by', 'amount_owed', 'status']
        read_only_fields = ['id', 'status']
