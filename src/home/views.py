from django.shortcuts import render

def index(request):
    base_template = "base_partial.html" if request.htmx else "base_complete.html"
    return render(
        request,
        "home/index.html",
        {
            "base_template": base_template
        }
    )