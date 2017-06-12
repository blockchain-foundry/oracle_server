import ast

from django import forms

from .models import Keystore


class SignForm(forms.Form):
    raw_tx = forms.CharField(required=True)
    script = forms.CharField(required=True)
    input_index = forms.IntegerField(required=True)
    sender_address = forms.CharField(required=True)
    multisig_address = forms.CharField(required=True)
    color = forms.CharField(required=True)
    amount = forms.IntegerField(required=True)


class MultisigAddrFrom(forms.Form):
    pubkey = forms.CharField(required=False)
    pubkey_list = forms.CharField(required=False)
    multisig_address = forms.CharField(required=True)
    is_state_multisig = forms.BooleanField(required=True)

    def clean(self):
        cleaned_data = super(MultisigAddrFrom, self).clean()
        pubkey = cleaned_data.get('pubkey')
        pubkey_list = cleaned_data.get('pubkey_list')

        if ((not pubkey and not pubkey_list)
                or (pubkey and pubkey_list)):
            raise forms.ValidationError(
                'Should have either one of `pubkey` or `pubkey_list`!'
            )
        return cleaned_data

    def get_pubkey(self):
        if self.cleaned_data.get('pubkey'):
            return self.cleaned_data.get('pubkey')
        elif self.cleaned_data.get('pubkey_list'):
            pubkey_list = self.cleaned_data.get('pubkey_list')
            keystore = Keystore.objects.get(public_key__in=pubkey_list)
            return keystore.public_key
        return None

    def clean_pubkey(self):
        pubkey = self.cleaned_data.get('pubkey')
        if pubkey:
            if not Keystore.objects.filter(public_key=pubkey).exists():
                raise forms.ValidationError(
                    'This public is not belonged to this orcale.'
                )
        return pubkey

    def clean_pubkey_list(self):
        pubkey_list = self.cleaned_data.get('pubkey_list')
        if pubkey_list:
            pubkey_list = ast.literal_eval(self.cleaned_data.get('pubkey_list'))
            if not Keystore.objects.filter(public_key__in=pubkey_list).exists():
                raise forms.ValidationError(
                    'No public is not belonged to this orcale.'
                )

        return pubkey_list


class NotifyForm(forms.Form):
    tx_hash = forms.CharField(max_length=100)
    subscription_id = forms.CharField(max_length=100)
