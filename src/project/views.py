from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from project.utils.decorators import group_required
import cloudinary
import json
from pprint import pprint

def health_check(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return HttpResponse(status=204)

@group_required("example")
def generate_cloudinary_upload_signature(request):
    return HttpResponse(cloudinary.utils.api_sign_request(json.loads(request.body), settings.CLOUDINARY_API_SECRET, "sha256"), content_type="text/plain")