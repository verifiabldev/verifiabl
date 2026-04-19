from __future__ import annotations

from workers import WorkerEntrypoint

_APP = None


def _app():
    global _APP
    if _APP is None:
        from main import app as fastapi_app

        _APP = fastapi_app
    return _APP


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(_app(), request, self.env)
