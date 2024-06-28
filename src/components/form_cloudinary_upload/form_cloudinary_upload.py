from django_components import component
from django.conf import settings
from django.urls import reverse
import time

@component.register("form_cloudinary_upload")
class PaginationNavigation(component.Component):
    template_name = "form_cloudinary_upload/template.html"

    def get_context_data(self, input_id, image_public_id=""):
        return {
            "cloudinary_upload_info": {
                "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
                "api_key": settings.CLOUDINARY_API_KEY,
                "generate_signature_url": reverse("cloudinary-upload-signature"),
                "input_id": input_id,
                },
            "image_public_id": image_public_id
        }

class Media:
    js = "script.js"