from django.contrib import admin
from BillManagement.models import Bill, BillSplit

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'created_by', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_by',)

@admin.register(BillSplit)
class BillSplitAdmin(admin.ModelAdmin):
    list_display = ('bill', 'paid_by', 'amount_paid', 'owed_by', 'amount_owed', 'status')
    search_fields = ('bill__title', 'paid_by__username', 'owed_by__username')
    list_filter = ('status',)
