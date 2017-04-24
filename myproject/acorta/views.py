from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from acorta.models import Urls
from django.views.decorators.csrf import csrf_exempt
import urllib.parse


# Create your views here.

@csrf_exempt
def acorta(request):
    listado = Urls.objects.all();
    if request.method == 'GET':
        if Urls.objects.all().exists():
            respuesta = "Urls acortadas:<br/>"
            for url in listado:
                respuesta += "*" + str(url.id) + " : " + url.url_larga + "<br/>"
        else:
            respuesta = "No hay Urls acortadas."

        respuesta += " Introduce una nueva Url larga: "
        respuesta += "<form method='POST' action=''><input type='text'" \
            " name='url_larga'><input type='submit' " \
            "value='Acortar'></form>"

    elif request.method == 'POST':
        url_larga = urllib.parse.unquote(request.POST['url_larga'])
        if (url_larga[0:7] != "http://" and url_larga[0:8] != "https://"):
            url_larga = "http://" + url_larga
        if url_larga in listado:
            url_corta = "/" + url_larga.id
        else:
            url = Urls(url_larga=url_larga)
            url.save()
            url_corta = Urls.objects.get(url_larga=url_larga).id
        respuesta = "La url acortada es " + str(url_corta)

    return HttpResponse(respuesta)

def redirect(request, url_corta):
    try:
        url_larga = Urls.objects.get(id=url_corta).url_larga
        return HttpResponseRedirect(url_larga)
    except Urls.DoesNotExist:
        respuesta = "Url no disponible"
        return HttpResponse(respuesta)
