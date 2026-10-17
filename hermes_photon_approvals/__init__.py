"""Photon approval transport for unchanged Hermes Agent."""


def register(ctx):
    from .config import Settings
    from .photon import PhotonSender
    from .transport import present

    def approval(request):
        settings = Settings.from_env()
        return present(request, settings, PhotonSender.from_env(settings.dm))

    ctx.register_approval_transport('photon-cards', approval)
