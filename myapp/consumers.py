# In consumers.py
from channels import Group
import json

# Store user session
global users
users = {}
# Status of # of users in the connection
global connectedUsers
connectedUsers = [] 
# Connected to websocket.connect

def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
#    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    # convert data to dict type
    content = json.loads(message.content['text'])
    # use method to process incoming message
    redirectData(content,message)

# Connected to websocket.disconnect
def ws_disconnect(message):
    connectedUsers.remove(users[hash(str(message.reply_channel))])
    Group(users[hash(str(message.reply_channel))]).discard(message.reply_channel)
    otherUser = connectedUsers.pop()
    print 'Informing the other user: %s' % otherUser
    jsonData = json.dumps({'type': 'leave'})
    sendData(otherUser,jsonData)


# Process and forwading information based on the message
def redirectData(data,message):
    # if the connection type is login
    if (data['type'] == "login"):
        print 'User is requesting to log in'
        # Inform user this name is already exist
        if data['name'] in users.values():
            jsonData = json.dumps({'type': "login",'success': False})
            sendData(data['name'],jsonData)

        # log user in and inform user 
        else:
            #users.append(data['name'])
            users[hash(str(message.reply_channel))] = data['name']
            Group(data['name']).add(message.reply_channel)
            jsonData = json.dumps({'type': 'login','success': True})
            sendData(data['name'],jsonData)      
            print "%s Added to Group" % data['name']

    # if the connection type is offer from user to another
    elif (data['type'] == "offer"):
        # If another user is logged in then forward this offer
        if data['name'] in users.values():
            print 'Forwarding offer to %s' % data['name']
            jsonData = json.dumps({'type': 'offer',
                                        'offer': data['offer'],
                                        'name': users[hash(str(message.reply_channel))]})
            sendData(data['name'],jsonData)

        # if another user is not found
        else:
            print '%s not found!' % data['name']

    # if the connection type is answer, then forward it to another
    elif (data['type'] == "answer"):
        print 'Forwarding answer to: %s' % data['name']
        jsonData = json.dumps({'type': 'answer',
                                        'answer': data['answer']})
        sendData(data['name'],jsonData)

        # Add both users to the current connection list
        # the other user
        if data['name'] not in connectedUsers:
                connectedUsers.append(data['name'])
        # the user who is sending this answer connection from
        if users[hash(str(message.reply_channel))]not in connectedUsers:
                connectedUsers.append(users[hash(str(message.reply_channel))])

    # if the connection type is candidate then forward to another
    elif (data['type'] == "candidate"):
        print 'Forwarding candidate to: %s' % data['name']
        print 'From: %s' % users[hash(str(message.reply_channel))]
        jsonData = json.dumps({'type': 'candidate',
                                        'candidate': data['candidate']})
        sendData(data['name'],jsonData)

    # if the an user is leaving then inform the other user
    elif (data['type'] == "leave"):
        print 'Disconnecting from: %s' % users[hash(str(message.reply_channel))]
        # remove the user from current connection list
        if connectedUsers.size:
            connectedUsers.remove(users[hash(str(message.reply_channel))])
            # get the other user name 
            otherUser = connectedUsers.pop()
        print 'Informing the other user: %s' % otherUser
        jsonData = json.dumps({'type': 'leave'})
        sendData(otherUser,jsonData)

        # if no user is in the connection session
        if len(connectedUsers) == 0:
            print "Connection is empty"
    # everything else say bye.
    else:
        message.reply_channel.send({
                    "text": json.dumps({'type': 'error',
                                        'message': 'Error: unknown information'})                
            })

def sendData(to,jsonData):
    Group(to).send({
            "text": jsonData
        })