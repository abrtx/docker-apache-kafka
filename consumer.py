from kafka import KafkaConsumer
import json

if __name__ == '__main__':

    consumer = KafkaConsumer(
        'message',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        api_version=(2, 8, 1),
    )

    for message in consumer:
        print(json.loads(message.value))
