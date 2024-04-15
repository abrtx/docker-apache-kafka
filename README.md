
# Table of Contents

1.  [Apache Kafka](#orgd5fae01)
    1.  [What is](#org8ebcc7e)
    2.  [Why?](#orgc67c37d)
    3.  [Main Kafka concepts](#org3a2644c)
        1.  [Topic](#orgceda933)
        2.  [Consumers](#org86deae7)
        3.  [Producers](#orgfcbd30c)
2.  [Install](#org60fa705)
    1.  [Docker-compose](#org990ed73)
        1.  [Run](#orgdf702cb)
        2.  [connect to shell docker](#orgd4bc1ee)
        3.  [create a topic (On Docker)](#orgb135c80)
        4.  [list of topics](#org548ba9a)
    2.  [Python](#org566a053)
        1.  [Package](#org31185b5)
        2.  [Example Local Mode](#orgab3d166)



<a id="orgd5fae01"></a>

# Apache Kafka


<a id="org8ebcc7e"></a>

## What is

Event streaming. It is the practice of capturing
data in `REAL-TIME` from event sources, and save
this in, for example a database.


<a id="orgc67c37d"></a>

## Why?

Syncronicity. Some time we need to maintain certain
data, our core data `ON-LINE` in multiples centers. 


<a id="org3a2644c"></a>

## Main Kafka concepts


<a id="orgceda933"></a>

### Topic

Category or stream name for the messages are published.


<a id="org86deae7"></a>

### Consumers

Client that `read` data from Kafka Topic


<a id="orgfcbd30c"></a>

### Producers

Client that `publish` data to Kafka Topic


<a id="org60fa705"></a>

# Install


<a id="org990ed73"></a>

## Docker-compose

    version: '3.7'
    
    services:
      zookeeper:
        image: wurstmeister/zookeeper
        container_name: zookeeper
        ports:
          - "2181:2181"
      kafka:
        image: wurstmeister/kafka
        container_name: kafka
        ports:
          - "9092:9092"
        environment:
          KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT
          KAFKA_ADVERTISED_LISTENERS: LISTENER_DOCKER_INTERNAL://kafka:9092,LISTENER_DOCKER_EXTERNAL://localhost:19092
          KAFKA_LISTENERS: LISTENER_DOCKER_INTERNAL://kafka:9092,LISTENER_DOCKER_EXTERNAL://localhost:19092
          KAFKA_INTER_BROKER_LISTENER_NAME: LISTENER_DOCKER_EXTERNAL
          KAFKA_CREATE_TOPICS: "message:1:1" # Instead of on Docker machine
          KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
        volumes:
          - "/etc/localtime:/etc/localtime:ro"


<a id="orgdf702cb"></a>

### Run

    docker compose up


<a id="orgd4bc1ee"></a>

### connect to shell docker

    docker exec -it kafka bash


<a id="orgb135c80"></a>

### create a topic (On Docker)

    /opt/kafka/bin#kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic messages


<a id="org548ba9a"></a>

### list of topics

    kafka-topics.sh --list --zookeeper zookeeper:2181


<a id="org566a053"></a>

## Python


<a id="org31185b5"></a>

### Package

    pip install kafka-python


<a id="orgab3d166"></a>

### Example Local Mode

Example from <https://youtu.be/LHNtL4zDBuk?si=c9jBgYLA-hirv254>

1.  Consumer

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

2.  Producer

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

3.  Logs

    1.  Consumer
    
            (kafka) abrtx@abrtx-laptop:~/work/docker/kafka$ python consumer.py 
            {'user_id': 64, 'recipient_id': 15, 'message': 'GcKbqxZENgaqlbDCRUYjYfhRoKpneRrZ'}
            {'user_id': 63, 'recipient_id': 46, 'message': 'fayKgujmREuibZoeWMBKJJCovutHYLkM'}
            {'user_id': 81, 'recipient_id': 95, 'message': 'KDxEHwrVwiHlecCtAgrRXsTHapQVtUfE'}
            {'user_id': 93, 'recipient_id': 76, 'message': 'ZldDAeYttjmPGgsBWyxPmSIrJtHblyBF'}
            {'user_id': 48, 'recipient_id': 87, 'message': 'RfVlkXaEMvzpBFnRkKBWKmycgWGffGwk'}
            {'user_id': 72, 'recipient_id': 52, 'message': 'fmdtuqecTYLhVKECLLjzKwDlnbPlhpZO'}
            {'user_id': 8, 'recipient_id': 69, 'message': 'EgFUcTOjjMhMzUtgiuJAwYjARKKiJgRT'}
    
    2.  Producer
    
            (kafka) abrtx@abrtx-laptop:~/work/docker/kafka$ python producer.py
            {'user_id': 64, 'recipient_id': 15, 'message': 'GcKbqxZENgaqlbDCRUYjYfhRoKpneRrZ'}
            {'user_id': 63, 'recipient_id': 46, 'message': 'fayKgujmREuibZoeWMBKJJCovutHYLkM'}
            {'user_id': 81, 'recipient_id': 95, 'message': 'KDxEHwrVwiHlecCtAgrRXsTHapQVtUfE'}
            {'user_id': 93, 'recipient_id': 76, 'message': 'ZldDAeYttjmPGgsBWyxPmSIrJtHblyBF'}
            {'user_id': 48, 'recipient_id': 87, 'message': 'RfVlkXaEMvzpBFnRkKBWKmycgWGffGwk'}
            {'user_id': 72, 'recipient_id': 52, 'message': 'fmdtuqecTYLhVKECLLjzKwDlnbPlhpZO'}
            {'user_id': 8, 'recipient_id': 69, 'message': 'EgFUcTOjjMhMzUtgiuJAwYjARKKiJgRT'}

