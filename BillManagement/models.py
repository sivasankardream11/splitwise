from django.db import models
import uuid
from user.models import UserInfo as UserProfile  # Assuming UserProfile is defined in the user app


class Debt(models.Model):
    """
    Model representing a debt between two users.
    """
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='from_user')  # User who lent the money
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='to_user')  # User who owes the money
    amount = models.IntegerField()  # The amount of money owed

    def __str__(self):
        return f'{self.to_user.name} owes {self.amount} to {self.from_user.name}'  # String representation of the debt


class Group(models.Model):
    """
    Model representing a group of users and their associated debts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique UUID for the group
    group_name = models.CharField(max_length=255, unique=True)  # Name of the group
    debts = models.ManyToManyField(Debt, null=True)  # Many-to-many relationship with Debt model
    members = models.ManyToManyField(UserProfile)  # Many-to-many relationship with UserProfile model

    def __str__(self):
        return self.group_name  # String representation of the group


class ExpenseUser(models.Model):
    """
    Model representing a user's financial involvement in an expense.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique UUID for each expense user
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # The user involved in the expense
    paid_share = models.IntegerField(default=0)  # Amount paid by the user
    owed_share = models.IntegerField(default=0)  # Amount the user owes
    net_balance = models.IntegerField(default=0)  # Net balance (paid - owed)

    def __str__(self):
        return f'{self.user.name} - Net Balance: {self.net_balance}'  # String representation of the user's balance


class Expense(models.Model):
    """
    Model representing an expense and its details.
    """
    name = models.CharField(max_length=255, unique=True)  # Name of the expense
    expense_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, db_constraint=False)  # Group associated with the expense
    description = models.CharField(max_length=255)  # Description of the expense
    payment = models.BooleanField(default=False)  # Whether the expense is fully paid
    amount = models.IntegerField()  # Total amount of the expense
    date = models.DateTimeField(auto_now_add=True)  # Date when the expense was created
    repayments = models.ManyToManyField(Debt)  # Many-to-many relationship with Debt model
    users = models.ManyToManyField(ExpenseUser)  # Many-to-many relationship with ExpenseUser model
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique transaction ID for the expense

    def __str__(self):
        return self.name  # String representation of the expense
