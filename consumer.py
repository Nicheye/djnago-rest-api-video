import pika,json, os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin.settings')
django.setup()
params = pika.URLParameters('amqps://uvdnjxcq:w4MgqecIXdohMwTGYLPdw4IHSztJlPpe@moose.rmq.cloudamqp.com/uvdnjxcq')
from products.models import Product
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='admin')

def callback(ch,method,properties,body):
    print('Revceived in admin')
    data = json.loads(body)
    print(data)
    product = Product.objects.get(id=data)
    product.like +=1
    product.save()
    print('Product likes increased')

channel.basic_consume(queue='admin',on_message_callback=callback, auto_ack=True)
print("Started consuming")
channel.start_consuming()
channel.close()