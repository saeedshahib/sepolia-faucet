from django.contrib import admin
from .models import FaucetTransaction


@admin.register(FaucetTransaction)
class FaucetTransactionAdmin(admin.ModelAdmin):
    list_display = ('address', 'ip_address', 'amount', 'status', 'created_at')
