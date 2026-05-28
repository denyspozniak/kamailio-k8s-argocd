"""Kamailio KSR routing module (app_python3).

Loaded by `cfgengine "python"` in kamailio.cfg. The `mod_init` function
returns an instance of `kamailio`, whose `ksr_request_route` method handles
every incoming SIP request.
"""

import KSR


ALLOWED_METHODS = ("INVITE", "ACK", "BYE", "CANCEL", "OPTIONS", "INFO")


def mod_init():
    KSR.info("kamailio3.py: module init\n")
    return Kamailio()


class Kamailio:
    def child_init(self, rank):
        return 0

    def ksr_request_route(self, msg):
        method = KSR.pv.get("$rm")
        ruri = KSR.pv.get("$ru")
        src = "%s:%s" % (KSR.pv.get("$si"), KSR.pv.get("$sp"))
        host = KSR.pv.get("$HN(n)")

        KSR.xlog.xinfo(
            "request: host=%s method=%s r-uri=%s from=%s\n"
            % (host, method, ruri, src)
        )

        if method not in ALLOWED_METHODS:
            KSR.sl.sl_send_reply(405, "Method Not Allowed")
            return 1

        if method == "OPTIONS":
            KSR.sl.sl_send_reply(200, "OK - %s" % host)
            return 1

        KSR.sl.sl_send_reply(200, "OK - %s" % host)
        return 1
