from bitrix24 import *


bx24 = Bitrix24('https://expertcentre.bitrix24.ru/rest/98/a1u9357630ogsjh2')

# print(bx24.callMethod('crm.product.list'))
# print(bx24.callMethod('crm.lead.list',
#                 filter={'PHONE': "79045914177"},
#                 select=['ID', 'TITLE', 'ASSIGNED_BY_ID',]))


api_request = bx24.callMethod('crm.lead.list',
                filter={'PHONE': "79038251234", 'EMAIL': "sokur-oksana@yandex.ru"},
                select=['ID', 'TITLE', 'ASSIGNED_BY_ID',])

# print(api_request)
# that = isinstance(api_request, list)
# print(that)
api_request = api_request[0]
id = api_request['ASSIGNED_BY_ID']
print(api_request['ID'])
print(api_request['TITLE'])
print(api_request['ASSIGNED_BY_ID'])

# api_request = str(api_request)
# # #


# for e in api_request:
#     print(e)

# result = json.loads(api_request)
# print(result.TITLE)
api_request_user = bx24.callMethod('user.get', filter={'ID': id})
api_request_user = api_request_user[0]
print(api_request_user['LAST_NAME'])

#565

# print(bx24.callMethod('crm.lead.fields'))

# print(bx24.callMethod('crm.lead.list',
#                 filter={'PHONE': "79045914177"},
#                 select=['ID', 'TITLE', 'ST']))

# print(bx24.callMethod('crm.lead.userfield.list'))
# id = 251369
#
# print(bx24.callMethod('crm.lead.get', 251369))

