from rest_framework import serializers
from . import models



class DebtSerializer(serializers.ModelSerializer):
    """
    Serializer for the Debt model.
    """
    class Meta:
        model = models.Debt  # Model to serialize
        fields = ('id', 'from_user', 'to_user', 'amount')  # Fields to include in the serialization


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.
    """
    class Meta:
        model = models.Group  # Model to serialize
        fields = ('id', 'group_name', 'debts', 'members')  # Fields to include in the serialization


class ExpenseUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the ExpenseUser model.
    """
    class Meta:
        model = models.ExpenseUser  # Model to serialize
        fields = ('id', 'paid_share', 'owed_share', 'net_balance')  # Fields to include in the serialization


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model.
    """
    class Meta:
        model = models.Expense  # Model to serialize
        fields = ('transaction_id', 'name', 'expense_group', 'description', 'payment',
                  'amount', 'date', 'repayments', 'users')  # Corrected field names to match the model
