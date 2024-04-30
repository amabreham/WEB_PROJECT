from twilio.rest import Client


account_sid = 'AC8e3f256fabbdcaae196039210140190e'
auth_token = 'deff77637090870c5f0bb1f9785f355b'

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='+19382536302',
    body = 'haystack',
    to='+251978481098' )

print(message.sid)