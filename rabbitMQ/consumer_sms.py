import pika
import time
import sys
import json
from bson import json_util
import os
import configparser

sys.path.append(os.getcwd())
from mongo import User

conf = configparser.ConfigParser()
conf.read('settings.ini')
host = conf.get('rabbit', 'host')
port = conf.get('rabbit', 'port')
login = conf.get('rabbit', 'login')
password = conf.get('rabbit', 'password')

def callback(ch, method, properties, body):
    message = json_util.loads(body.decode())
    user = User.objects(id=message['id_user'])
    user.update(message_sends=True)
    print(f"Received {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main(): 
    credentials = pika.PlainCredentials(login, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='queue_sms', durable=True)
    print('Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='queue_sms', on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    main()