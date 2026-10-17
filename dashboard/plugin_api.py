"""Mounted by Hermes behind its existing dashboard authentication middleware."""
from hermes_photon_approvals.api import make_router

router = make_router()
