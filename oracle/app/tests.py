import json
import mock
try:
    import http.client as httplib
except ImportError:
    import httplib

from django.test import TestCase

from app.models import Proposal

API_VERSION = '/api/v1'


class ProposeTest(TestCase):

    def setUp(self):
        super(ProposeTest, self).setUp()
        self.url = API_VERSION + '/proposals/'

    def test_proposal_without_multisig(self):
        response = self.client.get(self.url)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, httplib.OK)
        self.assertNotEqual(data.get('public_key'), None)

    def test_proposal_with_multisig(self):
        # Get a pubkey by calling api
        response = self.client.get(self.url)
        data = json.loads(response.content.decode('utf-8'))
        public_key = data.get('public_key')
        # Create a new proposal
        Proposal.objects.create(public_key=public_key,
                                multisig_address='34Qk88LLP4y4wRWDCCifJBujMA2CKkBUgh')

        # Get proposal with multisig
        response = self.client.get(self.url + '34Qk88LLP4y4wRWDCCifJBujMA2CKkBUgh/')
        data = json.loads(response.content.decode('utf-8'))
        public_key_2 = data.get('public_key')

        self.assertEqual(public_key, public_key_2)


class MultisigAddrTest(TestCase):

    def setUp(self):
        super(MultisigAddrTest, self).setUp()
        self.url = API_VERSION + '/multisigaddress/'

        # gen a new keystore
        response = self.client.get(API_VERSION + '/proposals/')
        data = json.loads(response.content.decode('utf-8'))
        test_public_key = data.get('public_key')

        self.sample_form = {
            'pubkey': test_public_key,
            'multisig_address': '36Q4vWxZ8co2h2UviEudacMwFadqL4TtBw'
        }

        Proposal.objects.create(public_key=test_public_key)

    def fake_make_multisig_address_file(self):
        pass

    def fake_get_callback_url(request, multisig_address):
        callback_url = "http://172.18.250.12:7788/addressnotify/" + multisig_address
        return callback_url

    def fake_subscribe_address_notification(self, multisig_address, callback_url, confirmation):
        subscription_id = "1"
        created_time = "2017-03-15"
        return subscription_id, created_time

    @mock.patch('app.views.get_callback_url', fake_get_callback_url)
    @mock.patch('gcoinapi.client.GcoinAPIClient.subscribe_address_notification', fake_subscribe_address_notification)
    def test_set_multisig_address(self):
        response = self.client.post(self.url, self.sample_form)
        self.assertEqual(response.status_code, httplib.OK)

    @mock.patch('app.views.get_callback_url', fake_get_callback_url)
    @mock.patch('gcoinapi.client.GcoinAPIClient.subscribe_address_notification', fake_subscribe_address_notification)
    def test_invalid_form(self):
        self.sample_form['multisig_address'] = ''
        response = self.client.post(self.url, self.sample_form)
        self.assertEqual(response.status_code, httplib.BAD_REQUEST)

    @mock.patch('app.views.get_callback_url', fake_get_callback_url)
    @mock.patch('gcoinapi.client.GcoinAPIClient.subscribe_address_notification', fake_subscribe_address_notification)
    def test_invalid_pubkey(self):
        self.sample_form[
            'pubkey'] = '048cfdd643a92b2681a753521c056838f3d104a91af3bf37104dba698b4c75c5025ab25d96b600fef2d105b3e005e6e4ae2c234a58f54a8683762b05fd59935052'
        response = self.client.post(self.url, self.sample_form)
        self.assertEqual(response.status_code, httplib.BAD_REQUEST)


class AddressNotifiedCase(TestCase):

    def setUp(self):
        self.url = API_VERSION + '/addressnotify/3NfaDCrVHqQyLWHkvJqyTeVyLoLCgmdLt7'

        self.sample_form = {
            'tx_hash': 'e68cb204f44239ecbfd0d945760f8b377d8d943b4ceb62daa6d284617fa4386b',
            'subscription_id': '1',
            'notification_id': '2'
        }

    def fake_deploy_contracts(tx_hash):
        return True

    def fake_deploy_contracts_failed(tx_hash):
        return False

    def test_address_notified_bad_request(self):
        self.response = self.client.post(self.url, {})
        self.assertEqual(self.response.status_code, httplib.NOT_ACCEPTABLE)

    @mock.patch('smart_contract_utils.models.StateInfo.update_with_tx_hash', fake_deploy_contracts)
    def test_address_notified(self):
        self.response = self.client.post(self.url, self.sample_form)
        self.assertEqual(self.response.status_code, httplib.OK)
