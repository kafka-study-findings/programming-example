import time

from kafka import KafkaConsumer,TopicPartition
import os
import traceback

brokers = os.getenv("brokers")
clientId = os.getenv("client-id")
groupId = os.getenv("group-id")
topic = os.getenv("topic")

print("Brokers: ", brokers, flush=True)
print("Client Id: ", clientId, flush=True)
print("Group Id: ", groupId, flush=True)
print("Topic: ", topic, flush=True)

consumer = KafkaConsumer(topic,
    bootstrap_servers=[brokers],
    client_id=clientId,
    group_id=groupId,
)

consumer.poll(100)
# consumer.seek_to_beginning() # read from beginning
# consumer.seek_to_end() # read next message since listening

# read from specific offset
# consumer.seek(TopicPartition('{topic name}', {partition_id}), {offset})

for msg in consumer:
    try:
        print("Offset: ", msg.offset, flush=True)
        print("key: ", msg.key.decode("utf-8"), flush=True)
        print("value: ", msg.value.decode("utf-8"), flush=True)
        for header in msg.headers:
            print(f"{header[0]}: {header[1].decode('utf-8')}", flush=True)
    except Exception as ex:
        print("error", ex, flush=True)
        traceback.print_exc()
