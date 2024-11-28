import sys
import KSR as KSR

def ksr_request_route():
    KSR.sl.sl_send_reply(200, "Ok --$HN(n)")
    KSR.xlog.xwarn(" start debug me \n")
    KSR.warn("===== method [%s] r-uri [%s]\n" % (KSR.pv.get("$rm"),KSR.pv.get("$ru")))

    try:
        ip = requests.get('https://api.ipify.org').text
    except:
        ip = "Failed to resolve"

    if ksr_route_reqinit()==-255 :
        return 1

    return 1

def ksr_route_reqinit():
    KSR.set_reply_no_connect()
    KSR.force_rport()
    return 1

def dumpObj(obj):
    for attr in dir(obj):
        KSR.warn("obj.%s = %s\n" % (attr, getattr(obj, attr)))

def mod_init():
    KSR.warn("initializing python module\n")
    return 1
