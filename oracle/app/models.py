from django.db import models
from django.utils.crypto import get_random_string

from gcoin import (pubtoaddr, privtopub, sha256)

# class Oracle(models.Model):
#   created = models.DateTimeField(auto_now_add=True)
#   name = models.CharField(max_length=100, blank=True, default='')
#   url = models.TextField(validators=[URLValidator()])

#   class Meta:
#       ordering = ('created',)


class KeystoreQuerySet(models.query.QuerySet):

    def create_new_keypair(self, is_default=False):
        private_key = sha256(get_random_string(64, '0123456789abcdef'))
        public_key = privtopub(private_key)
        keystore = self.create(private_key=private_key,
                               public_key=public_key, is_default=is_default)
        return keystore

    def get_default_keypair(self):
        try:
            keystore = self.get(is_default=True)
        except Keystore.DoesNotExist:
            keystore = self.create_new_keypair(is_default=True)

        return keystore


class Keystore(models.Model):
    public_key = models.CharField(max_length=200)
    private_key = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    objects = KeystoreQuerySet.as_manager()


class OraclizeContract(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    interface = models.TextField()
    byte_code = models.TextField()

    class Meta:
        ordering = ('address',)


class Proposal(models.Model):
    public_key = models.CharField(max_length=200)
    multisig_address = models.CharField(max_length=100, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    is_state_multisig = models.BooleanField(default=False)

    class Meta:
        ordering = ('public_key',)

    def as_dict(self):
        return {
            'public_key': self.public_key,
            'multisig_address': self.multisig_address,
            'is_state_multisig': self.is_state_multisig
        }
