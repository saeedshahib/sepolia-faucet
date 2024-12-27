from rest_framework import serializers
from .models import FaucetTransaction


class FaucetTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaucetTransaction
        fields = '__all__'
