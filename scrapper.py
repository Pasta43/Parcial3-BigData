import boto3
import csv
import ntpath
from bs4 import BeautifulSoup

destinationBucket= "resultsnewspaperbucket"
def scrapping(fullPath,fileName,newspaper,soup,s3):
    """
    Function that saves the scrapping results from an newspaper html file.
    Firstly, this creates a csv file in a temporaly folder, and starts finding the title, 
    the section and the url from every news item in the html file depending of the newspaper. 

    
    Parameters:
    - fullPath: that contains the full path from the saved file in a s3 bucket with an associated event
    - fileName: that contains just file name
    - newspaper: that contains the newspaper name
    - soup: that is an BeautifulSoup instance
    - s3: that contains a boto3 resource instance to manage s3
    """
    csvFile = open('/tmp/'+fileName+'.csv', 'w',encoding='utf-8')
    writer = csv.writer(csvFile,dialect='unix')
    row=['title','section','url']
    writer.writerow(row)

    if(newspaper=="El_tiempo"):
        articles=soup.find_all('article')
        for article in articles:
            category_anchor=article.find("a",{'class':'category'})
            title_anchor= article.find("a",{'class':'title'})
            if(category_anchor and title_anchor):
                category=category_anchor.getText()
                title=title_anchor.getText()
                url='https://www.eltiempo.com'+title_anchor.get('href')
                row=[title,category,url]
                writer.writerow(row)
    elif(newspaper=="El_espectador"):
        articles=soup.findAll('div',{'class':'Card-Container'})
        for article in articles:
            category_div=article.find("h4",{'class':'Card-Section'})
            title_div= article.find("h2",{'class':'Card-Title'})
            if(category_div and title_div):
                category_anchor = category_div.find("a")
                category=category_anchor.getText()
                title_anchor = title_div.find("a")
                title=title_anchor.getText()
                url='https://www.elespectador.com'+title_anchor.get('href')
                row=[title,category,url]
                writer.writerow(row)
    csvFile.close()
    underFolders = fullPath.replace('headlines/raw','')
    s3.meta.client.upload_file('/tmp/'+fileName+'.csv', destinationBucket,'news/final'+underFolders+'.csv')


def handler(event, context):
    """
    Function that handles an s3 upload event.

    Parameters:
    - event: that contains the information about the event.
    - context: that represents the execution context of the lambda function
    """
    bucketName= event['Records'][0]['s3']['bucket']['name']
    fileName=event['Records'][0]['s3']['object']['key']
    fileName=fileName.replace('%3D','=')
    s3 = boto3.resource('s3')
    justFileName=ntpath.basename(fileName)   
    s3.meta.client.download_file(bucketName, fileName, '/tmp/'+justFileName)
    f = open('/tmp/'+justFileName,'r',encoding='utf-8')
    txt=f.read()
    soup = BeautifulSoup(txt,'html.parser')
    if("El_tiempo" in fileName):
        scrapping(fileName,justFileName,"El_tiempo",soup,s3)
    elif("El_espectador" in fileName):
        scrapping(fileName,justFileName,"El_espectador",soup,s3)
    repairTable()
    return {
        'statusCode': 200,
        'body': 'Logs generated!'
    }

def repairTable():

    client = boto3.client('athena')

    config = {
        'OutputLocation': 's3://' + destinationBucket + '/news/final',
        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}

    }

    # Query Execution Parameters
    sql = 'MSCK REPAIR TABLE newspapers.news'
    context = {'Database': 'newspapers'}

    client.start_query_execution(QueryString = sql, 
                                 QueryExecutionContext = context,
                                 ResultConfiguration = config)