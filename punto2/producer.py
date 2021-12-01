from kafka import KafkaProducer
import time
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
f = open("SPY_TICK_TRADE.csv",encoding='utf-8')
i=0
count=0
print('Sending batch',count)
for row in f:
    toSend= row.split(',')[1]
    producer.send('quickstart-events',bytes(toSend,encoding='utf-8'))
    i+=1
    if(i==100):
        time.sleep(20)
        count+=1
        print('Sending batch',count)
        i=0
producer.flush()