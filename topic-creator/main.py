import os
import time
import traceback

from pyChaining import Chains
from progress_utils_xh import ProgressPinger
from kafka import KafkaAdminClient
from kafka.admin import NewTopic


if __name__ == '__main__':
    print(os.environ, flush=True)
    brokers = os.getenv("hosts")
    print("Broker from env: ", brokers, flush=True)

    topics = []
    with open("topic_list.txt") as f:
        for line in f.readlines():
            topic = line.strip("\n")
            print(f"Add topic[{line}]", flush=True)
            topics.append(line.rstrip("\n"))
    topics = Chains.of(topics).filter(lambda x: x!="").list()
    i = 0
    while True:
        print(f"retry for {i} time{'s' if i > 1 else ''}", flush=True)
        i += 1
        try:
            print(brokers, flush=True)
            admin = KafkaAdminClient(
                bootstrap_servers=brokers,
                client_id="test-client"
            )
            existingTopic = admin.list_topics()
            print("Existing topic ",existingTopic, flush=True)
            topic_list = Chains.of(topics).\
                filter(lambda x: x not in existingTopic).\
                map(lambda x: NewTopic(x, num_partitions=1, replication_factor=1)).\
                list()

            if len(topic_list) == 0:
                print("Complete creating all topics", flush=True)
                break
            else:
                print(f"{len(topic_list)} topics to create", flush=True)
                rs = admin.create_topics(new_topics=topic_list)
                print(rs, flush=True)
        except Exception as ex:
            print("err", flush=True)
            print(ex, flush=True)
            traceback.print_exc()
            pass
        time.sleep(2)
    print("Done", flush=True)
