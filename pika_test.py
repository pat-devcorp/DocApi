import pika
credentials = pika.PlainCredentials('guest', 'guest')
# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials)  # Replace with your RabbitMQ host
)
channel = connection.channel()

# Declare the queue for messages (if it doesn't already exist)
channel.queue_declare(queue='test')  # Replace with your desired queue name

# Message to be sent
message = 'Hello, world!'

# Publish the message to the queue
channel.basic_publish(exchange='',  # Use default exchange
                       routing_key='test',
                       body=message)

print("Message sent to RabbitMQ queue!")

# Close the connection
connection.close()
