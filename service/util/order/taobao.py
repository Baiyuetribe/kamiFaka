import top

req=top.api.AppstoreSubscribeGetRequest(url,port)
req.set_app_info(top.appinfo(appkey,secret))

req.nick="tbtest110"
req.lease_id=14192

resp= req.getResponse()
print(resp)


