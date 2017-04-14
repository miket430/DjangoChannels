# In consumers.py
from channels import Group
import json

global users
users = {}
# Connected to websocket.connect

def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
#    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    global users
    content = json.loads(message.content['text'])
    print ""
    print message.reply_channel

    redirectData(content,message)
    '''
    username = content['name']
    if username not in users:
        users.append(username)
        if (username == 'user1'):
            Group("user1").add(message.reply_channel)
            print "user1 Added to Group"
        else:
            Group("user2").add(message.reply_channel)
            print "user2 Added to Group"
    if (username == 'user2'):
        Group("user1").send({
            "text": "[user] %s" % content,
        })

'''
# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def redirectData(data,message):
    global users
    if (data['type'] == "login"):
        print 'User is requesting to log in'
        if data['name'] in users.values():
            Group("%s" % data['name']).send({
                    json.dumps({'type': "login",'success': False})
                })
        else:
            #users.append(data['name'])
            users[str(message.reply_channel)] = data['name']
            Group("%s" % data['name']).add(message.reply_channel)      
            Group("%s" % data['name']).send({
                    "text": json.dumps({'type': 'login','success': True})
                })
            print "%s Added to Group" % data['name']

    elif (data['type'] == "offer"):
        if data['name'] in users.values():
            print 'Forwarding offer to %s' % data['name']
            Group("%s" % data['name']).send({
                    "text": json.dumps({'type': 'offer',
                                        'offer': data['offer'],
                                        'name': users[str(message.reply_channel)]})
                })

        else:
            print '%s not found!' % data['name']
    elif (data['type'] == "answer"):
        print 'Forwarding answer to: %s' % data['name']
        Group("%s" % data['name']).send({
                    "text": json.dumps({'type': 'answer',
                                        'answer': data['answer']})
                })
    elif (data['type'] == "candidate"):
        print 'Forwarding candidate to: %s' % data['name']
        print 'From: %s' % users[str(message.reply_channel)]
        Group("%s" % data['name']).send({
                    "text": json.dumps({'type': 'candidate',
                                        'candidate': data['candidate']})
                })
    elif (data['type'] == "leave"):
        pass
    else:
        pass