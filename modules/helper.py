import json
# Using bson to create quick and dirty unique salt id's
from bson import ObjectId

def renderJSON(o, callback=None):
    try:
        if callback:
            return "%s(%s);" % (callback, json.dumps(o, ensure_ascii=False, sort_keys=False))
        else:
            return json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2)
    except TypeError:
        print(o)
        raise

def checkCookie(web):
    userSalt = web.get_secure_cookie("salt")
    if userSalt is None:
        userSalt = web.set_secure_cookie("salt", str(ObjectId()))
    
    return userSalt


def setheaders(web, r=1):
    web.set_header("Allow", "GET, POST, DELETE, PUT, HEAD")
    web.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, HEAD")
    web.set_header("Access-Control-Allow-Headers", "Accept-Encoding, Authorization, X-Requested-With, Content-Type, Origin, Accept")
    web.set_header("Access-Control-Allow-Credentials", "true")
    web.set_header("Access-Control-Expose-Headers", "Content-Type, Content-Length, Date")
    if r == 1:
        web.set_header("Content-Type", "application/json")
    else:
        web.set_header("Content-Type", "text/html")

    web.set_header("P3P", 'CP="IDC DSP COR CURa ADMa OUR IND PHY ONL COM STA')