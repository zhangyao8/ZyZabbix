from django.shortcuts import render
from django.shortcuts import HttpResponse
from ZyZabbix import zabbix_get
from ZyZabbix import zbconfig


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


def addHost(request):
    if request.method == 'POST':
        clientip = request.POST.get('clientip')
        clientport = request.POST.get('clientport')
        hostname = request.POST.get('hostname')
        visiblename = request.POST.get('visiblename', None)
        groups = request.POST.get('groups')
        templates = request.POST.get('templates')
        zapi = zbconfig.login_zabbix()['zapi']
        ret = zapi.host.create(host=hostname,
                               name=visiblename,
                               interfaces=[
                                   {"type": 1, "main": 1, "useip": 1, "ip": clientip, "dns": "", "port": clientport}],
                               groups=[{"groupid": groups}], templates=[{"templateid": templates}])
        return HttpResponse(ret)


def zabbixSettings(request):
    if request.method == "GET":
        ret = zbconfig.login_zabbix()
        return render(request, 'settings.html', ret)

    if request.method == "POST":
        zbconfig.readInfo()
        dic = {
            'zabbix_web': request.POST.get('zabbixurl'),
            'zabbix_user': request.POST.get('zabbixuser'),
            'zabbix_pass': request.POST.get('zabbixpass'),
            'zabbix_server': request.POST.get('zabbixip'),
        }

        for k, v in dic.items():
            if v:
                zbconfig.setInfo(k, v)
        zbconfig.writeInfo()
        return HttpResponse('success')
