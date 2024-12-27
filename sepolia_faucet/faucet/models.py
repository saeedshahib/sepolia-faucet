from django.db import models
from django.conf import settings

from .exceptions import FaucetException

from web3 import Web3


class FaucetTransaction(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1
        SUCCESS = 2
        FAILED = 3
        ERROR = 4

    address = models.CharField(max_length=42)
    ip_address = models.GenericIPAddressField()
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    status = models.PositiveIntegerField(choices=Status.choices, default=Status.PENDING.value)
    tx_hash = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def send_transaction(self):
        nonce = 1
        if FaucetTransaction.objects.exists():
            nonce = FaucetTransaction.objects.last().id + 1
        web3 = Web3(Web3.HTTPProvider(settings.SEPOLIA_RPC_URL))
        tx = {
            'nonce': nonce,
            'to': self.address,
            'value': web3.to_wei(self.amount, 'ether'),
            'gas': 21000,
            'gasPrice': web3.to_wei('10', 'gwei'),
        }
        signed_tx = web3.eth.account.sign_transaction(tx, settings.FAUCET_PRIVATE_KEY)
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        except Exception as e:
            print(e)
            self.status = FaucetTransaction.Status.FAILED.value
            self.save(update_fields=['status'])
            raise FaucetException(message=str(e))

        self.tx_hash = tx_hash.hex()
        self.status = FaucetTransaction.Status.SUCCESS.value
        self.save(update_fields=['tx_hash', 'status'])
