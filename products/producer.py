#
import pika, json
params = pika.URLParameters('amqps://uvdnjxcq:w4MgqecIXdohMwTGYLPdw4IHSztJlPpe@moose.rmq.cloudamqp.com/uvdnjxcq')

connection = pika.BlockingConnection(params)

channel = connection.channel()
def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='admin',body=json.dumps(body) , properties=properties)