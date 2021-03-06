import json
import threading
import os
from time import sleep

COMMANDS = """
1. Get list of rooms
2. Subscribe to room
3. Send message in room
4. Get all messages of room
5. Show all subscriptions
6. Unsubscribe from room
7. All messages from all subscriptions
8. Exit
"""


class Send(threading.Thread):
    """
        Поток отправлки сообщений пользователя на сервер
    """
    def __init__(self, sock, name, client):
        super().__init__()
        self.sock = sock
        self.name = name
        self.client = client

    def run(self):
        """
            Прием вводв пользователя.
            Перенаправление данных на необходимые методы.
        """
        while True:
            sleep(0.5)
            print(COMMANDS)
            command_id = input('Type number: ')

            if command_id == "1":
                self.get_rooms_list()
            elif command_id == "2":
                self.subscribe()
            elif command_id == "3":
                self.send_message_in_room()
            elif command_id == "4":
                self.get_message_from_room()
            elif command_id == "5":
                self.get_all_subscribes()
            elif command_id == "6":
                self.unsubscribe()
            elif command_id == "7":
                self.all_messages()
            elif command_id == "8":
                self.sock.close()
                os._exit(0)
            else:
                print('You type something strange:( \nTry again')

    def get_rooms_list(self):
        """
            Отправка запроса на получение всех комнат на сервере
            :return :  {"command_id": 1}
        """
        data = {"command_id": 1}

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def get_message_from_room(self, room=None):
        """
            Отправка запроса на получение всех сообщений из комнаты
            :return: {
                "command_id": 4,
                "data": {"room_name": "...",
                         "nick": self.client.rooms.get(room)}
                }
        """
        if room is None:
            room = input('Input room name: ')

        if not self.client.rooms.get(room, False):
            print('You unsubscribe on this room')
            return

        data = {
                "command_id": 4,
                "data": {"room_name": room,
                         "nick": self.client.rooms.get(room)}
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def subscribe(self):
        """
            Отправка запроса на подписку а комнату
            :return {
                "command_id": 2,
                "data": {
                         "room_name": "...",
                         "nick": "..."
                         }
                }
        """
        room = input('Input room name: ')
        nick = input('Input your nick in this room: ')

        if self.client.rooms.get(room, False):
            print('You have already subscribed on this room')
            return

        data = {
                "command_id": 2,
                "data": {
                         "room_name": room,
                         "nick": nick
                         }
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def unsubscribe(self):
        """
            Отправка запроса на отподписку от комнату
            :return {
                "command_id": 6,
                "data": {
                         "room_name": "...",
                         "nick": "..."
                         }
                }
        """
        room = input('Input room name: ')

        if not self.client.rooms.get(room, False):
            print('You don`t subscribed on this room')
            return

        nick = self.client.rooms.get(room)
        data = {
                "command_id": 6,
                "data": {
                         "room_name": room,
                         "nick": nick
                         }
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def send_message_in_room(self):
        """
            Отправка сообщения в комнату
            :return {
                "command_id": 3,
                "data": {"room_name": room,
                         "nick": nick,
                         "message": message}
                }
        """
        room = input('Input room name: ')
        message = input('Message: ')

        if not self.client.rooms.get(room, False):
            print('You unsubscribe on this room')
            return

        nick = self.client.rooms.get(room, False)

        data = {
                "command_id": 3,
                "data": {"room_name": room,
                         "nick": nick,
                         "message": message}
                }

        data = json.dumps(data)
        data = data.encode()

        self.sock.sendall(data)

    def get_all_subscribes(self):
        """
            Информация о всех подписоках
            Информация берется со стороны клиента и с сервером не взаимодействует
        """
        print('Your subscribes:\n')

        for room in self.client.rooms:
            print(room)

    def all_messages(self):
        """
            Вывод все сообщений всех подписанных комнат
            Используется метод для получения всех комнат и инфромация о подписках на стороне клиента
        """
        for room in self.client.rooms:
            self.get_message_from_room(room)
