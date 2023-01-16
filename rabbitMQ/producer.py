# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
import pika
import sys
from bson import json_util
import os
import faker
import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')
host = conf.get('rabbit', 'host')
port = conf.get('rabbit', 'port')
login = conf.get('rabbit', 'login')
password = conf.get('rabbit', 'password')

sys.path.append(os.getcwd())
from mongo import User

def seeds():
    User.drop_collection()
    fake = faker.Faker()
    for _ in range(5):
        User(
            firstname = fake.first_name(), 
            lastname = fake.last_name(),
            email = fake.email(),
            phone = fake.phone_number(),
            method = 'email'
            ).save()
    for _ in range(5):
        User(
            firstname = fake.first_name(), 
            lastname = fake.last_name(),
            email = fake.email(),
            phone = fake.phone_number(),
            method = 'sms'
            ).save()

def get_users():
    return User.objects(message_sends=False)

def add_message_to_queue(mes, user, queue, channel):
    message = {
        'id_user': user.id,
        'fullname': ' '.join([user.firstname, user.lastname]),
        'email': user.email,
        'message': mes
    }
    channel.basic_publish(
        exchange='ex_message',
        routing_key=queue,
        body=json_util.dumps(message).encode(),
        properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
    print(" [x] Sent ", mes)

def main():
    credentials = pika.PlainCredentials(login, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='ex_message', exchange_type='direct')
    channel.queue_declare(queue='queue_email', durable=True)
    channel.queue_declare(queue='queue_sms', durable=True)
    channel.queue_bind(exchange='ex_message', queue='queue_email')
    channel.queue_bind(exchange='ex_message', queue='queue_sms')

    users = get_users()
    mes = ' '.join(sys.argv[1:])
    for el in users:
        if el.method == 'email':
            add_message_to_queue(mes, el, 'queue_email', channel)
        if el.method == 'sms':
            add_message_to_queue(mes, el, 'queue_sms', channel)

    connection.close()
    
if __name__ == '__main__':
    seeds()
    main()