from django.contrib import admin

from .models import Keystore, Proposal


@admin.register(Keystore)
class KeystoreAdmin(admin.ModelAdmin):
    list_display = ('is_default', 'public_key', 'private_key')


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('is_state_multisig', 'public_key', 'multisig_address')
