import time
import json
import random
from data_generator import generate_message
from kafka import KafkaProducer


if __name__ == '__main__':

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        api_version=(2, 8, 1),
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    while True:
        dummy_message = generate_message()
        print(f'{str(dummy_message)}')
        producer.send('message', dummy_message)
        time_to_sleep = random.randint(1, 11)
        time.sleep(time_to_sleep)
