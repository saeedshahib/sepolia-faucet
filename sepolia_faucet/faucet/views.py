from django.db.models import Count, Case, When
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FaucetTransaction
from .exceptions import FaucetException

from decimal import Decimal
from web3 import Web3

from .serializers import FaucetTransactionSerializer


class FundView(APIView):
    def post(self, request):
        recipient = request.data.get('address')
        ip_address = self.get_client_ip(request)
        amount = Decimal('0.0001')

        if not Web3.is_address(recipient):
            return Response({"error": "Invalid Ethereum address."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            faucet_transaction = FaucetTransaction.objects.create(
                address=recipient,
                ip_address=ip_address,
                amount=amount,
            )
            faucet_transaction.send_transaction()
            serializer = FaucetTransactionSerializer(faucet_transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FaucetException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class StatsView(APIView):

    @staticmethod
    def get(request):
        from datetime import timedelta
        from django.utils.timezone import now

        one_day_ago = now() - timedelta(hours=24)

        stats = (
            FaucetTransaction.objects.filter(created_at__gte=one_day_ago)
            .aggregate(
                success_count=Count(Case(When(status=FaucetTransaction.Status.SUCCESS.value, then=1))),
                failed_count=Count(Case(When(status=FaucetTransaction.Status.FAILED.value, then=1))),
            )
        )

        return Response({
            "successful_transactions": stats["success_count"],
            "failed_transactions": stats["failed_count"],
        })
