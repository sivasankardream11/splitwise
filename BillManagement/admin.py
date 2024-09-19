from django.contrib import admin
from BillManagement import models  # Importing models from BillManagement app

# Registering the Debt model to make it accessible in the admin interface
admin.site.register(models.Debt)

# Registering the Group model to make it accessible in the admin interface
admin.site.register(models.Group)

# Registering the Expense model to make it accessible in the admin interface
admin.site.register(models.Expense)

# You can also customize the admin interface for these models if needed by creating custom admin classes
