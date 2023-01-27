import time

from kafka import KafkaProducer
import os

brokers = os.getenv("brokers")
clientId = os.getenv("client-id")
topic = os.getenv("topic")

print("Brokers: ", brokers, flush=True)
print("Client Id: ", clientId, flush=True)
print("Topic: ", topic, flush=True)

producer = KafkaProducer(
    bootstrap_servers=[brokers],
    client_id=clientId,
    acks='all'
)

i = 0
while True:
    i+=1
    headers = [('version', b'1.0.0')]
    key = b'python-producer'
    value = f"[{i}]Hello world from {clientId}!!!".encode("utf-8")
    result = producer.send(topic, value=value, key=key, headers=headers).get()
    time.sleep(2)

# producer.close() # infinite loop
