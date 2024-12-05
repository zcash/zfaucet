from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

import re
from datetime import *

from pyZcash.rpc.ZDaemon import *
from faucet.models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('HTTP_X_REAL_IP')
    return ip

def index(request):
    # TODO: Going to show the page no matter what, so pull these variables out.
    if HealthCheck.objects.latest('timestamp'):
        hc = HealthCheck.objects.latest('timestamp')
        t_balance = hc.t_balance
        z_balance = hc.z_balance
        print(("T balance", t_balance))
        print((" z balance", z_balance))
        balance = {'transparent': t_balance, 'private': z_balance}
        difficulty = hc.difficulty
        height = hc.height
        payouts = Drip.objects.count()
    else:
        balance = '0'
        difficulty = '0'
        height = '0'

    zd = ZDaemon()
    version = zd.getVersion()

    #If it is a post, an address was submitted.
    if request.method == 'POST':
        # Check IP and payout address
        # This is the old workaround, added get_client_ip
        ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            ip = request.META.get('HTTP_X_REAL_IP')
        ip = get_client_ip(request)
        address = request.POST.get('address', '')
        print(("IP: ", ip))
        print(("address: ", address))
        try:
            last_payout = Drip.objects.filter(Q(ip=ip) | Q(address=address)).order_by('-timestamp')[0]
            now = datetime.utcnow().replace(tzinfo=timezone.get_current_timezone())
            timesince = (now - last_payout.timestamp).total_seconds()

            # TODO: keep track of sessions as well, track one per session?

            if timesince < (60*60*12):
                msg = "Sorry, you received a payout too recently.  Come back later."
                return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})

        except (Drip.DoesNotExist, IndexError) as e:
            # Nothing in queryset, so we've never seen this ip and address before (individually)
            pass

        # zd = ZDaemon()
        try:
            uaddrs = zd.z_listaccounts()
            sender = uaddrs[0]['addresses'][0]['ua']
            msg = ''
            opid = zd.z_sendmany(sender, address, 1.0, msg)
            print(("OPID", opid))
            if opid != None and 'opid' in opid:
                    resp = zd.z_getoperationstatus(opid)
                    print(("Operation status response:", resp))
                    print(("operation status: ", resp[0]['status']))
                    #why is it not working when it's executing?
                    if resp[0]['status'] == 'executing':
                        msg = "Sent! Get the status of your private payout with z_getoperationstatus '[\"{0}\"]'.".format(opid)
                        return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
                    if resp[0]['status'] == 'failed':
                        msg = "Operation failed for {0}. Error message: {1}".format(opid, resp[0]['error']['message'])
                        return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})
        except Exception as e:
            # TODO: Give better error if faucet is empty!
            print(e)
            print("IN ERROR")
            msg = "Issue sending transaction.  Is your address correct?"
            return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':True, 'message':msg})


    return render(request, 'faucet/faucet.html', {'version':version,'balance':balance,'difficulty':difficulty,'height':height, 'payouts':payouts, 'flash':False, 'message':""})
