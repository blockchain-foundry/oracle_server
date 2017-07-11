from django.contrib import admin

from .models import StateInfo, ContractInfo


@admin.register(StateInfo)
class StateInfoAdmin(admin.ModelAdmin):
    list_display = ('multisig_address', 'latest_tx_time', 'latest_tx_hash')


@admin.register(ContractInfo)
class ContractInfoAdmin(admin.ModelAdmin):
    list_display = ('multisig_address', 'contract_address')
