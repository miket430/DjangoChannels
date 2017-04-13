# In consumers.py
from channels import Channel,Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
import json

users = {}
# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("chat").add(message.reply_channel)
    print "hhhhhhhhhhhhhhhhhhhh"
    print message.user.username
    print "555555555555555555555555555"

@channel_session_user
# Connected to websocket.receive
def ws_message(message):
    content = message.content['text']
    print json.loads(content)['name']
    print '6666666666666666666666666666'
    print message.user.username
    message.channel_session.send({
        "text": message.content['text'],
    })
#    Group("chat").send({
#        "text": "[user] %s" % message.content['text'],
#    })

@channel_session_user
# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
