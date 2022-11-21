import os 
from google.cloud import pubsub_v1
crepential_path= os.getcwd()+"/"+"miso-4cloud-769393b6b084.json"
print(crepential_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crepential_path

subscriber=pubsub_v1.SubscriberClient()
sub_path='projects/miso-4cloud/subscriptions/convert-sub'
def convert(message):
    print(message)
    print(message.data)
    message.ack

streaming_pull_future=subscriber.subscribe(sub_path,callback=convert)

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
