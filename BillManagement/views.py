from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from BillManagement import models, serializers
from user.models import UserInfo as UserProfile


class CreateGroupApiView(APIView):
    """Group Creation View"""
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Creates a group and adds members"""
        members_emails = request.data.get('members', [])
        member_ids = []

        for email in members_emails:
            try:
                user = UserProfile.objects.get(email=email)
                member_ids.append(user.id)
            except UserProfile.DoesNotExist:
                return Response({'error': f'User with email {email} does not exist!'},
                                status=status.HTTP_400_BAD_REQUEST)

        request.data['members'] = member_ids
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Group "{serializer.data.get("group_name")}" created successfully'},
                            status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AddUserToGroupApiView(APIView):
    """Add member to existing group"""
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Adds a user to a group"""
        group_name = request.data.get('group_name')
        user_email = request.data.get('user_email')
        try:
            user = UserProfile.objects.get(email=user_email)
            group = models.Group.objects.get(group_name=group_name)
        except (UserProfile.DoesNotExist, models.Group.DoesNotExist):
            return Response({'error': 'User or Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user in group.members.all():
            return Response({'message': 'User is already a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

        group.members.add(user)
        return Response({'message': f'User "{user_email}" added to group "{group.group_name}" successfully'},
                        status=status.HTTP_200_OK)


class ShowGroupMembersApiView(APIView):
    """Show group members"""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """Displays members of a group"""
        group_name = request.GET.get('name')
        try:
            group = models.Group.objects.get(group_name=group_name)
            members = [str(member) for member in group.members.all()]
            return Response({'members': members}, status=status.HTTP_200_OK)
        except models.Group.DoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ShowUserDetailsApiView(APIView):
    """Show user details"""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        user_email = request.GET.get('email')
        try:
            user = UserProfile.objects.get(email=user_email)
            debts_from = models.Debt.objects.filter(from_user=user)
            debts_to = models.Debt.objects.filter(to_user=user)
            debt_summary = {}
            total_debt = 0
            total_credit = 0

            for debt in debts_from:
                debt_summary[debt.to_user.name] = debt_summary.get(debt.to_user.name, 0) - debt.amount
                total_debt -= debt.amount
            for debt in debts_to:
                debt_summary[debt.from_user.name] = debt_summary.get(debt.from_user.name, 0) + debt.amount
                total_credit += debt.amount

            summary = [
                f'User "{user.name}" owes {amount} to "{user}"' if amount > 0 else f'User "{user.name}" is owed {-amount} by "{user}"'
                for user, amount in debt_summary.items() if amount != 0
            ]

            return Response({
                'user': str(user),
                'total_debt': total_debt,
                'total_credit': total_credit,
                'debt_summary': summary
            }, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class CreateExpenseApiView(APIView):
    """Expense Creation View"""
    serializer_class = serializers.ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Creates an expense and assigns it to users"""
        description = request.data.get('description')
        users_emails = request.data.get('users', [])
        paid_by_email = request.data.get('paid_by')
        amount = request.data.get('amount')
        group_name = request.data.get('group_name', None)
        expense_name = request.data.get('name')

        if models.Expense.objects.filter(name=expense_name).exists():
            return Response({'error': 'Expense name must be unique'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            users = UserProfile.objects.filter(email__in=users_emails)
            paid_by_user = UserProfile.objects.get(email=paid_by_email)
            group = models.Group.objects.get(group_name=group_name) if group_name else None
        except (UserProfile.DoesNotExist, models.Group.DoesNotExist):
            return Response({'error': 'User or Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

        share_per_user = amount / len(users)
        expense_users = []
        repayments = []

        for user in users:
            if user != paid_by_user:
                debt = models.Debt.objects.create(from_user=paid_by_user, to_user=user, amount=share_per_user)
                repayments.append(debt)
            expense_user = models.ExpenseUser.objects.create(
                user=user,
                paid_share=share_per_user if user == paid_by_user else 0,
                owed_share=share_per_user,
                net_balance=-share_per_user if user != paid_by_user else amount - share_per_user
            )
            expense_users.append(expense_user)

        expense = models.Expense.objects.create(
            expense_group=group,
            description=description,
            amount=amount,
            name=expense_name
        )
        expense.repayments.set(repayments)
        expense.users.set(expense_users)
        expense.save()
        return Response({'message': 'Expense created successfully'}, status=status.HTTP_201_CREATED)


class ShowGroupDetailsApiView(APIView):
    """Show group details"""
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        group_name = request.GET.get('name')
        try:
            group = models.Group.objects.get(group_name=group_name)
            expenses = models.Expense.objects.filter(expense_group=group, payment=False)
            expense_details = [
                {
                    "name": expense.name,
                    "description": expense.description,
                    "repayments": [str(rep) for rep in expense.repayments.all() if
                                   rep.from_user != rep.to_user and rep.amount != 0]
                } for expense in expenses
            ]
            return Response({'expenses': expense_details}, status=status.HTTP_200_OK)
        except models.Group.DoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)


class DeleteUserApiView(APIView):
    """Delete user"""
    permission_classes = [IsAuthenticated]

    def delete(self, request) -> Response:
        user_email = request.GET.get('email')
        try:
            user = UserProfile.objects.get(email=user_email)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class DeleteGroupApiView(APIView):
    """Delete group"""
    permission_classes = [IsAuthenticated]

    def delete(self, request) -> Response:
        group_name = request.GET.get('name')
        try:
            group = models.Group.objects.get(group_name=group_name)
            group.delete()
            return Response({'message': 'Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except models.Group.DoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)


class RecordPaymentApiView(APIView):
    """Record payment"""
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        from_user_email = request.data.get('from_user')
        to_user_email = request.data.get('to_user')
        amount = request.data.get('amount')
        group_name = request.data.get('group_name')
        expense_name = request.data.get('expense_name')

        try:
            from_user = UserProfile.objects.get(email=from_user_email)
            to_user = UserProfile.objects.get(email=to_user_email)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if group_name:
            try:
                expense = models.Expense.objects.get(name=expense_name)
                group = models.Group.objects.get(group_name=group_name)
            except (models.Expense.DoesNotExist, models.Group.DoesNotExist):
                return Response({'error': 'Expense or Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

            if expense.expense_group != group:
                return Response({'error': 'Expense is not associated with this group'},
                                status=status.HTTP_400_BAD_REQUEST)

            for repayment in expense.repayments.all():
                if repayment.from_user == to_user and repayment.to_user == from_user:
                    if repayment.amount < amount:
                        return Response({'error': 'Insufficient repayment amount'}, status=status.HTTP_400_BAD_REQUEST)
                    repayment.amount -= amount
                    repayment.save()
                    break
            else:
                debt = models.Debt.objects.create(from_user=to_user, to_user=from_user, amount=amount)
                expense.repayments.add(debt)

            expense.save()
            if all(rep.amount <= 0 for rep in expense.repayments.all()):
                expense.payment = True
                expense.save()
            return Response({'message': 'Expense payment recorded successfully'}, status=status.HTTP_200_OK)
