# Parcial3 BigData
## This repository includes 2 items
---

### Punto 1
In this folder, you will see a program that downloads the main pages of https://www.eltiempo.com/ and https://www.publimetro.co/ and another that makes scrapping of those pages and save them in an s3 bucket. On the other hand, in AWS glue they will be included in 2 jobs to work simultaneously and finally it will be used a crawler that allow to see the results in AWS Athena.

To use locally, you have to setup:

```
pip install -r requirements.txt
```

To upload the libraries used in this item, you have to generate a .whl file. All the necessary is in: https://aws.amazon.com/premiumsupport/knowledge-center/glue-import-error-no-module-named/ 

### Punto 2

In this folder, you will see two programs: producer and consumer, working over kafka and java JDK 8. The producer reads a csv file that contains the price of an action and with the consumer it will be processed in order to get the minimum price, the maximum price, the average price and the standard deviation. 

To install the requirements:

```
pip install -r requirements.txt
```

It is mandatory keep running a kafka server, zookeeper and create a topic for subscribe both programs. 
