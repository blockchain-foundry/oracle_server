from django.conf.urls import url

from .views import (CheckContractCode, DumpContractState, GetBalance,
                    GetStorage, NewTxNotified, Proposes,
                    Multisig_addr, Sign, AddressNotified)

urlpatterns = [
    url(r'^proposals/$', Proposes.as_view()),
    url(r'^proposals/(?P<multisig_address>[a-zA-Z0-9]+)/', Proposes.as_view()),
    url(r'^signnew/', Sign.as_view()),
    url(r'^sign/', Sign.as_view()),
    url(r'^multisigaddress/', Multisig_addr.as_view()),
    url(r'^storage/(?P<multisig_address>[a-zA-Z0-9]+)/', GetStorage.as_view()),
    url(r'^states/(?P<multisig_address>[a-zA-Z0-9]+)/$', DumpContractState.as_view()),
    url(r'^balance/(?P<multisig_address>[a-zA-Z0-9]+)/(?P<address>[a-zA-Z0-9]+)$',
        GetBalance.as_view()),
    url(r'^getcontract/(?P<multisig_address>[a-zA-Z0-9]+)/', CheckContractCode.as_view()),
    url(r'^notify/(?P<tx_hash>[a-zA-Z0-9]+)', NewTxNotified.as_view()),
    url(r'^addressnotify/(?P<multisig_address>[a-zA-Z0-9]+)(|/)$', AddressNotified.as_view()),
]
