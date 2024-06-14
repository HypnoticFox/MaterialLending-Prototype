from django.http import HttpResponse
from django.db import connection

def health_check(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return HttpResponse(status=204)