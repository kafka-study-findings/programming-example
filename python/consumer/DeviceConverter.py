import json

from kafka import KafkaConsumer, KafkaProducer
import os
import traceback
import pymysql.cursors


def start():
    conn = pymysql.connect(
        host="localhost",
        port=3307,
        user="root",
        password="my-secret-pw",
        database="device_status_db",
        cursorclass=pymysql.cursors.DictCursor
    )

    brokers = os.getenv("brokers")
    clientId = os.getenv("client-id")
    groupId = os.getenv("group-id")
    topic = os.getenv("topic-in")
    topicOut = os.getenv("topic-out")

    print("Brokers: ", brokers, flush=True)
    print("Client Id: ", clientId, flush=True)
    print("Group Id: ", groupId, flush=True)
    print("Topic: ", topic, flush=True)

    consumer = KafkaConsumer(topic,
                             bootstrap_servers=[brokers],
                             client_id=clientId,
                             group_id=groupId,
                             )

    producer = KafkaProducer(bootstrap_servers=[brokers],
                             client_id=clientId,
                             acks='all'
                             )

    consumer.poll(100)
    # consumer.seek_to_beginning() # read from beginning
    # consumer.seek_to_end() # read next message since listening

    # read from specific offset
    # consumer.seek(TopicPartition('{topic name}', {partition_id}), {offset})

    for msg in consumer:
        try:
            offset = msg.offset
            key = msg.key.decode("utf-8")
            value = msg.value.decode("utf-8")
            print("Offset: ", offset, flush=True)
            print("key: ", key, flush=True)
            print("value: ", value, flush=True)
            valueDict = json.loads(value)

            with conn.cursor() as cur:
                cur.execute("select * from last_device_status where id=%s", key)
                rs = cur.fetchone()
                if rs:
                    cur = conn.cursor()
                    cur.execute("update last_device_status set value_last=%s where id=%s", (valueDict['datetime'], key))
                else:
                    producer.send(topicOut, key=b"new-device", value=msg.key)
                    cur = conn.cursor()
                    cur.execute("insert into last_device_status (id, value_last, value_processed) value (%s, %s, '')",
                                (key, valueDict['datetime']))
                conn.commit()
        except Exception as ex:
            print("error", ex, flush=True)
    traceback.print_exc()
