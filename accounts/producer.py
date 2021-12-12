# import pika, json

# #params = pika.URLParameters('amqps://yzsvrisk:h3TK19Z4XhV2CtxCV5CYDuly-ZieJeb6@woodpecker.rmq.cloudamqp.com/yzsvrisk')

# # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# # channel = connection.channel()


# # def publish(method, body):
# #     properties = pika.BasicProperties(method)
# #     channel.basic_publish(exchange='', routing_key='accounts', body=json.dumps(body), properties=properties)

# #----------------------------RabbitMQ CLOUD VERSION----------------------------------------------------#
# # publish.py
# import pika, os

# # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
# url = os.environ.get('amqps://yzsvrisk:h3TK19Z4XhV2CtxCV5CYDuly-ZieJeb6@woodpecker.rmq.cloudamqp.com/yzsvrisk', 'amqp://guest:guest@localhost:5672/%2f')
# params = pika.URLParameters(url)
# connection = pika.BlockingConnection(params)
# channel = connection.channel() # start a channel
# channel.queue_declare(queue='accounts') # Declare a queue
# def publish(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(exchange='', routing_key='accounts', body=json.dumps(body), properties=properties)

