import sys
#import Router.Logger as Logger
import KSR as KSR

def mod_init():
    KSR.warn("===== from Python mod init\n")
    dumpObj(KSR)
    return kamailio()

class kamailio:
    def __init__(self):
        KSR.warn('===== kamailio.__init__\n')


    # executed when kamailio child processes are initialized
    def child_init(self, rank):
        KSR.warn('===== kamailio.child_init(%d)\n' % rank)
        return 0


    # SIP request routing
    # -- equivalent of request_route{}
    def ksr_request_route(self, msg):
        KSR.sl.sl_send_reply(200, "Ok --$HN(n)")
        KSR.xlog.xwarn(" start debug me \n")
        KSR.warn("===== method [%s] r-uri [%s]\n" % (KSR.pv.get("$rm"),KSR.pv.get("$ru")))

        try:
            ip = requests.get('https://api.ipify.org').text
        except:
            ip = "Failed to resolve"

        if self.ksr_route_reqinit(msg)==-255 :
            return 1

        return 1

    def ksr_route_reqinit(self, msg):
        return -255

def dumpObj(obj):
    for attr in dir(obj):
        KSR.warn("obj.%s = %s\n" % (attr, getattr(obj, attr)))

