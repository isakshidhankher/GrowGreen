# # chat/consumers.py
# import json
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))


#  chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.http import request
from .models import *

class ChatConsumer(WebsocketConsumer):

    def message_to_json(self, message):
        return {
            'author':message.contact.user.username,
            'content': message.text,
            'timestamp':str(message.timestamp)
        }

    def messages_to_json(self, messages):
        # to make json version of messages
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    
    def fetch_messages(self, data):
        # print('fetch')
        # cont = Contact.objects.filter(user = self.scope['user']).first()
        print("idhar aya")
        print(data['id'])
        
        obj = Chat.objects.filter(id = data['id']).first()
        # messages = "test"
        # messages = obj.messages.all()
        messages = obj.last_30_messages()
        print(messages)
        content = {
            'room_id':data['id'],
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        # self.send_message(content)
        self.send(text_data = json.dumps(content))
        
    def new_message(self, data):
        author = data['from']
        # author = 'ap'
        # contact = Contact.object.get(user__usernamectes = data['author'])
        # obj = Chat.object.get(id = data['room_id'])
        
        # author_user = User.objects.filter(username = author)[0]
        # message = Message.objects.create(author = author_user, text = data['message'])
        contact = Contact.objects.get(user__username = data['from'])
        obj = Chat.objects.filter(id = data['room_id']).first()
        msg = Message(contact = contact, text = data['message'])
        msg.save()
        # obj.save()
        obj.messages.add(msg)
        
        content = {
            'command':'new_message',
            'message':self.message_to_json(msg)
        }
        print(content["message"])
        return self.send_chat_messages(content)
    
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
    }
    
    # def chat_list(self):
    #     obj = Chat.objects.filter(participants__user = request.user)
    #     # you can also use get_object_or_404 it is very easy to use as well
        
    #     chat_list = []
    #     for i in obj:
    #         print(i.participants.all()[0].user, i.id)
    #         chat_list.append([i.participants.all()[0], i.id])
        
    #     # print(dir(obj))
    #     print(chat_list)

            
    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        # data = 'new_message'
        print('.............',data['command'])
        self.commands[data['command']](self,data)


    def send_chat_messages(self, message):

        # message = data['message']

        # Send message to room group using channel layer
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        # self.send(text_data = json.dumps(message))


    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        self.send(text_data = json.dumps(message))

    def send_message(self, message):
        self.send(text_data = json.dumps(message))



    def connect(self):
        print("idhar aya")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
