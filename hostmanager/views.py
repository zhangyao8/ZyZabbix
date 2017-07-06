from django.shortcuts import render
from django.shortcuts import HttpResponse
from ZyZabbix import zabbix_get

def index(request):
    return render(request, 'index.html')

def hostadd(request):
    return render(request, 'hostadd.html')

def zabbixCheck(request):
    if request.method == 'POST':
        clientip = request.POST.get('clientip')
        clientport = request.POST.get('clientport')
        ret = zabbix_get.gethostname(clientip, clientport)
        return HttpResponse(ret)

