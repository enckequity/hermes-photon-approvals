"""Validate outgoing JSON against the installed official Photon proto contract."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from hermes_photon_approvals.photon import PhotonSender


class PhotonSchemaTests(unittest.TestCase):
    def test_live_card_matches_official_send_and_update_messages(self):
        grpcurl = os.environ.get('PHOTON_APPROVAL_GRPCURL')
        protos = os.environ.get('PHOTON_APPROVAL_PROTO_DIR')
        if not grpcurl or not protos:
            self.skipTest('Set the pinned grpcurl and official proto paths for schema qualification.')
        from google.protobuf import descriptor_pb2, descriptor_pool, json_format, message_factory
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'schema.pb'
            subprocess.run([grpcurl, '-import-path', protos, '-proto',
                            'photon/imessage/v1/message_service.proto', '-protoset-out', str(output),
                            'describe', 'photon.imessage.v1.MessageService'],
                           check=True, capture_output=True, timeout=10)
            descriptors = descriptor_pb2.FileDescriptorSet.FromString(output.read_bytes())
        pool = descriptor_pool.DescriptorPool()
        for descriptor in descriptors.file:
            pool.Add(descriptor)
        card = PhotonSender._card('https://agent.example.test/photon-approvals?request=r1', 'Review a command')
        payloads = {
            'SendCustomizedMiniAppMessageRequest': {**card, 'chatGuid': 'any;-;+15555550123',
                                                    'clientMessageId': '14b952e5-780b-43dc-98af-eab0f157fbfa'},
            'UpdateCustomizedMiniAppMessageRequest': {**card, 'session': {
                'chatGuid': 'any;-;+15555550123', 'sessionId': 's',
                'messageGuid': 'm', 'targetMessageGuid': 'm'}},
        }
        for name, body in payloads.items():
            message = message_factory.GetMessageClass(pool.FindMessageTypeByName('photon.imessage.v1.'+name))()
            json_format.ParseDict(body, message)
