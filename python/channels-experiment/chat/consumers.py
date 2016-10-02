from django.shortcuts import render_to_response
from channels import Group
from channels.handler import AsgiHandler
from channels.sessions import channel_session

def http_consumer(message):
    response = render_to_response('index.html')

    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session
def ws_connect(message):
    # get room name
    room = message.content['path'].strip('/')
    message.channel_session['room'] = room
    # add WS reply channel to the room
    Group('chat-' + room).add(message.reply_channel)


@channel_session
def ws_message(message):
    # send the jsonified message to the room
    room = message.channel_session['room']
    Group('chat-' + room).send({'text': message['text']})


@channel_session
def ws_disconnect(message):
    # detach the socket from the room
    room = message.channel_session['room']
    Group('chat-' + room).discard(message.reply_channel)
