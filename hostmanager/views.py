from django.shortcuts import render
from django.shortcuts import HttpResponse
from ZyZabbix import zabbix_get
from ZyZabbix import zbconfig
from ZyZabbix import pyzabbix


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


def zabbixSettings(request):
    if request.method == "GET":
        zbconfig.read_info()
        zabbixurl = zbconfig.get_info('zabbix_web')
        zabbixsess = zbconfig.get_info('zabbix_sess')
        zabbixuser= zbconfig.get_info('zabbix_user')
        zabbixpass = zbconfig.get_info('zabbix_pass')
        zabbixip = zbconfig.get_info('zabbix_server')
        zabbixstatus = 1
        zapi = pyzabbix.ZabbixAPI(zabbixurl)
        zapi.auth = zabbixsess
        result = zapi.user.get(countOutput=1)
        if "error" in result:
            zabbixsess = zapi.login(zabbixuser, zabbixpass)
            if zabbixsess == "error":
                zabbixstatus = 0
            else:
                zbconfig.set_info('zabbix_sess', zabbixsess)
                zbconfig.write_info()

        dic = {
            'zabbixurl': zabbixurl,
            'zabbixuser': zabbixuser,
            'zabbixpass': zabbixpass,
            'zabbixip': zabbixip,
            'zabbixsess': zabbixsess,
            'zabbixstatus': zabbixstatus,
        }
        return render(request, 'settings.html', dic)

    if request.method == "POST":
        zbconfig.read_info()
        dic = {
            'zabbix_web': request.POST.get('zabbixurl'),
            'zabbix_user': request.POST.get('zabbixuser'),
            'zabbix_pass': request.POST.get('zabbixpass'),
            'zabbix_server': request.POST.get('zabbixip'),
            'zabbix_sess' : request.POST.get('zabbixsess')
        }

        for k, v in dic.items():
            if v:
                zbconfig.set_info(k, v)
        zbconfig.write_info()
        return HttpResponse('success')