"""Run inside a supported Hermes environment, without starting a service."""
import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from hermes_cli.plugin_validate import validate_plugin_dir
from hermes_cli.plugins import PluginManager
from hermes_constants import set_hermes_home_override, reset_hermes_home_override

ROOT = Path(__file__).resolve().parents[1]

class NativeTests(unittest.TestCase):
    def test_native_manifest_validator_and_real_manager_registration(self):
        report = validate_plugin_dir(str(ROOT))
        self.assertTrue(report.ok, report.failures)
        with tempfile.TemporaryDirectory() as home:
            plugins = Path(home)/'plugins'
            plugins.mkdir()
            shutil.copytree(ROOT,plugins/'photon-approvals',ignore=shutil.ignore_patterns('.git','__pycache__'))
            (Path(home)/'config.yaml').write_text('plugins:\n  enabled: [photon-approvals]\n  isolation: in_process\n')
            manager = PluginManager(scope_key=home)
            try:
                manager.discover_and_load()
                token = set_hermes_home_override(home)
                try:
                    entry = manager.get_approval_transport('photon-cards')
                finally:
                    reset_hermes_home_override(token)
                self.assertIsNone(manager.get_approval_transport('photon-cards'))
                self.assertIsNotNone(entry, {k: {"error": v.error, "enabled": v.enabled} for k,v in manager._plugins.items() if k == "photon-approvals"})
                self.assertEqual(entry.plugin_id,'photon-approvals')
                self.assertEqual(entry.profile_home,str(Path(home).resolve()))
            finally:
                manager.unload()

    def test_dashboard_backend_exports_native_router(self):
        spec=importlib.util.spec_from_file_location('approval_dashboard_test',ROOT/'dashboard/plugin_api.py')
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        paths={route.path for route in module.router.routes}
        self.assertEqual(paths,{'/requests/{request_id}','/requests/{request_id}/decision'})

    def test_native_dashboard_mount_preserves_plugin_paths(self):
        import json
        from fastapi import FastAPI
        from hermes_cli.web_server_dashboard import _dashboard_plugin_entry, _mount_one_plugin_api
        raw=json.loads((ROOT/'dashboard/manifest.json').read_text())
        plugin=_dashboard_plugin_entry(raw,'photon-approvals',ROOT/'dashboard','user')
        app=FastAPI()
        self.assertTrue(_mount_one_plugin_api(app,plugin,{'photon-approvals'},set()))
        paths={route.path for route in app.routes}
        self.assertIn('/api/plugins/photon-approvals/requests/{request_id}',paths)
        self.assertIn('/api/plugins/photon-approvals/requests/{request_id}/decision',paths)
