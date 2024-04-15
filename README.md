
# Table of Contents

1.  [Apache Kafka](#orgac1b404)
    1.  [What is](#org8b09ae6)
    2.  [Why?](#orgb5223d6)
    3.  [Main Kafka concepts](#orge26d099)
        1.  [Topic](#org3ef4533)
        2.  [Consumers](#org41a3458)
        3.  [Producers](#org88f529b)
2.  [Install](#org1cc8d9d)
    1.  [Docker-compose](#org7a624e4)
        1.  [Run](#orga67615a)
        2.  [connect to shell docker](#orgacf4e8f)
        3.  [create a topic (On Docker)](#orgeba50ed)
        4.  [list of topics](#org7005ec7)
    2.  [Python](#orgc83fd47)
        1.  [Package](#orgadec498)
        2.  [Example Local Mode](#org979b8cb)



<a id="orgac1b404"></a>

# Apache Kafka


<a id="org8b09ae6"></a>

## What is

Event streaming. It is the practice of capturing
data in `REAL-TIME` from event sources, and storing
this in, for example a database.


<a id="orgb5223d6"></a>

## Why?

Syncronicity. Some time we need to maintain certain
data, our core data `ON-LINE` in multiples centers. 


<a id="orge26d099"></a>

## Main Kafka concepts


<a id="org3ef4533"></a>

### Topic

Category or stream name for the messages are published.


<a id="org41a3458"></a>

### Consumers

Client that `read` data from Kafka Topic


<a id="org88f529b"></a>

### Producers

Client that `publish` data to Kafka Topic


<a id="org1cc8d9d"></a>

# Install


<a id="org7a624e4"></a>

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


<a id="orga67615a"></a>

### Run

    docker compose up


<a id="orgacf4e8f"></a>

### connect to shell docker

    docker exec -it kafka bash


<a id="orgeba50ed"></a>

### create a topic (On Docker)

    /opt/kafka/bin#kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic messages


<a id="org7005ec7"></a>

### list of topics

    kafka-topics.sh --list --zookeeper zookeeper:2181


<a id="orgc83fd47"></a>

## Python


<a id="orgadec498"></a>

### Package

    pip install kafka-python


<a id="org979b8cb"></a>

### Example Local Mode

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

