from django.shortcuts import render


def handler403(request, *args, **kwargs):
    return render(request, 'handlers/403.html', status=403)


def handler404(request, *args, **kwargs):
    return render(request, 'handlers/404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, 'handlers/500.html', status=500)
