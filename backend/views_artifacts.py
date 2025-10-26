from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView

class ArtifactView(APIView):
    def get(self, request, name: str):
        path = Path(settings.MEDIA_ROOT) / "artifacts" / name
        if not path.exists():
            raise Http404("artifact not found")
        return FileResponse(open(path, "rb"))