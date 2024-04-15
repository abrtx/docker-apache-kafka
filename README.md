
# Table of Contents

1.  [Apache Kafka](#orgf1efc15)
    1.  [What is](#org36dc46a)
    2.  [Why?](#orgcd95a67)
    3.  [Main Kafka concepts](#org66650e5)
        1.  [Topic](#org7ae636e)
        2.  [Consumers](#orgaad4c99)
        3.  [Producers](#org5371b97)
2.  [Install](#org8690233)
    1.  [Docker-compose](#org109010d)
        1.  [Run](#orga93447a)
        2.  [connect to shell docker](#org89f00e1)
        3.  [create a topic (On Docker)](#org4d77050)
        4.  [list of topics](#org2736ffa)
    2.  [Python](#orgdb77f04)
        1.  [Package](#org9aad9b5)
        2.  [Example Local Mode](#org4c527f6)



<a id="orgf1efc15"></a>

# Apache Kafka


<a id="org36dc46a"></a>

## What is

Event streaming. It is the practice of capturing
data in `REAL-TIME` from event sources, and save
this in, for example a database.


<a id="orgcd95a67"></a>

## Why?

Syncronicity. Some time we need to maintain certain
data, our core data `ON-LINE` in multiples centers. 


<a id="org66650e5"></a>

## Main Kafka concepts


<a id="org7ae636e"></a>

### Topic

Category or stream name for the messages are published.


<a id="orgaad4c99"></a>

### Consumers

Client that `read` data from Kafka Topic


<a id="org5371b97"></a>

### Producers

Client that `publish` data to Kafka Topic


<a id="org8690233"></a>

# Install


<a id="org109010d"></a>

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


<a id="orga93447a"></a>

### Run

    docker compose up


<a id="org89f00e1"></a>

### connect to shell docker

    docker exec -it kafka bash


<a id="org4d77050"></a>

### create a topic (On Docker)

    /opt/kafka/bin#kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic messages


<a id="org2736ffa"></a>

### list of topics

    kafka-topics.sh --list --zookeeper zookeeper:2181


<a id="orgdb77f04"></a>

## Python


<a id="org9aad9b5"></a>

### Package

    pip install kafka-python


<a id="org4c527f6"></a>

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

