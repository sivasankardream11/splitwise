from django.urls import path
from . import views

urlpatterns = [
    # Group-related endpoints
    path('groups/create/', views.CreateGroupApiView.as_view(), name='create_group'),
    path('groups/add_user/', views.AddUserToGroupApiView.as_view(), name='add_user_to_group'),
    path('groups/members/', views.ShowGroupMembersApiView.as_view(), name='show_group_members'),
    path('groups/delete/', views.DeleteGroupApiView.as_view(), name='delete_group'),
    path('groups/details/', views.ShowGroupDetailsApiView.as_view(), name='show_group_details'),

    # Expense-related endpoints
    path('expenses/create/', views.CreateExpenseApiView.as_view(), name='create_expense'),
    path('expenses/record_payment/', views.RecordPaymentApiView.as_view(), name='record_payment'),
]
