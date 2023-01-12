# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
import pika
from datetime import datetime
import sys
import json
import os
import faker

sys.path.append(os.getcwd())
from mongo import SendsMessages, User

def seeds():
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

def get_message(message):
    mes = SendsMessages.objects.get(message=message)
    if not mes:
        users = User.objects()
        mes = SendsMessages(message=message, users=users)
        mes.save()
    return mes

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='ex_message', exchange_type='direct')
    channel.queue_declare(queue='queue_email', durable=True)
    channel.queue_declare(queue='queue_sms', durable=True)
    channel.queue_bind(exchange='ex_message', queue='queue_email')
    channel.queue_bind(exchange='ex_message', queue='queue_sms')

    mes_list = get_message(' '.join(sys.argv[1:]))
    for el in mes_list.users:
        if el.method == 'email':
            message = {
                'fullname': ' '.join([el.firstname, el.lastname]),
                'email': el.email,
                'message': mes_list.message
            }
            channel.basic_publish(
                exchange='ex_message',
                routing_key='queue_email',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        if el.method == 'sms':
            message = {
                'fullname': ' '.join([el.firstname, el.lastname]),
                'phone': el.phone,
                'message': mes_list.message
            }
            channel.basic_publish(
                exchange='ex_message',
                routing_key='queue_sms',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent ", message)
    connection.close()
    
if __name__ == '__main__':
    # seeds()
    main()