from django.http import HttpResponse


def ping(request):
    return HttpResponse("ok", status=200)
