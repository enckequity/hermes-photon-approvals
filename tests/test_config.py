import unittest
from hermes_photon_approvals.config import Settings

class ConfigTests(unittest.TestCase):
    def test_https_origin_and_fixed_dm_required(self):
        env = dict(PHOTON_APPROVAL_TENANT_ID='tenant-a', PHOTON_APPROVAL_PUBLIC_URL='https://agent.example.test',
                   PHOTON_APPROVAL_PROVIDER='oidc', PHOTON_APPROVAL_USER_ID='alice', PHOTON_APPROVAL_ORG_ID='org-a',
                   PHOTON_APPROVAL_DM='+15555550123', PHOTON_APPROVAL_STATE_DIR='/tmp/approval-test-state')
        self.assertEqual(Settings.from_env(env).identity, ('oidc','alice','org-a'))
        for url in ['http://agent.example.test','https://user:pass@agent.example.test','https://agent.example.test/?token=bad',
                    'https://agent.example.test/path','https://agent.example.test/#token', 'https://agent.example.test\\@evil.test']:
            with self.assertRaises(ValueError):
                Settings.from_env({**env, 'PHOTON_APPROVAL_PUBLIC_URL':url})
        for dm in ['group:abc', 'any;-;group', '+1', 'https://evil.test']:
            with self.assertRaises(ValueError):
                Settings.from_env({**env, 'PHOTON_APPROVAL_DM':dm})
