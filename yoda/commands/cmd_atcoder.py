import click
from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import csv
import pandas as pd
import numpy as np
import datetime 
import calplot
import matplotlib.pyplot as plt
handle=""
langExtension="cpp"
pathDir='/home/nm/CP-Solutions/'
pathDir+='Atcoder/'
curDir='/home/nm/Code/Statify/'
scrappedTill=0
def getHandle():
    global handle
    global pathDir
    global scrappedTill
    global curDir
    f=open(curDir+'AtcoderCount.txt','a')
    f.close()
    with open(curDir+'AtcoderCount.txt') as f:
        somethingInteresting=f.readlines()
        if somethingInteresting!=[]:
            scrappedTill=(int(somethingInteresting[0]))
    f=open(curDir+'handleAc.txt','a')
    f.close()
    with open(curDir+'handleAc.txt') as f:
        somethingInteresting=f.readlines()
        if somethingInteresting==[]:
            return
        handle=str(somethingInteresting[0])
    pathDir='/home/nm/CP-Solutions/Atcoder/'+handle+'/'
    
def changeHandle(han):
    global handle
    global scrappedTill
    global pathDir
    if handle==han:
        saveHandle()
        return
    handle=han
    saveHandle()
    scrappedTill=0
    pathDir='/home/nm/CP-Solutions/Atcoder/'+handle+'/'

def saveHandle():
    global handle
    global curDir
    with open(curDir+'handleAc.txt','w') as f:
        f.write(handle)
 
def getLang(lang):
    global langExtension
    if('GNU' in lang or "++" in lang or "GCC" in lang):
        langExtension="cpp"
    elif "C#" in lang:
        langExtension="cs"
    elif 'D' in lang:
        langExtension='d'
    elif 'Go' in lang:
        langExtension='go'
    elif  "Java" in lang:
        langExtension='java'
    elif "Kotlin" in lang:
        langExtension="kt"
    elif "Py" in lang:
        langExtension='py'
    elif 'JavaScript' in lang or 'JS' in lang  or 'js' in lang:
        langExtension='js'
    elif 'Scala' in lang:
        langExtension='scala'
    elif 'Ruby' in lang:
        langExtension='rb'
    elif 'Rust' in lang: 
        langExtension='rs'
    else:
        langExtension='txt'
    return langExtension
@click.group()
def cli():
    """👋 Get your Data from AtCoder!!🚀"""
    getHandle() 
    han=input("Enter your Prestigious AtCoder handle: ")
    changeHandle(han)
@cli.command('graph', short_help='Get your Submisssion Heatmap!!')
def graph():
    global handle
    global curDir
    curTime=0
    submission_list = []
    cnt  = set()
    while 1:
        r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user='+handle+'&from_second='+str(curTime))
        jsondata = r.json()
        if jsondata!=[]:
            for data in jsondata:
                timestamp = datetime.datetime.utcfromtimestamp(data["epoch_second"]).date()
                probem_name = data['problem_id']
                curTime=data["epoch_second"]+1
                if(data["result"]=="AC" and probem_name not in cnt):
                    date = timestamp
                    cnt.add(probem_name)
                    submission_list.append(date)
        else:
            if curTime == 0:
                click.secho('Handle entered does not exist ❌ or the Api is currently down 🛌',fg='red')
                return 
            else:
                break
    data_file = open(curDir+'atcoder.csv', 'w')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(["Date","Submissions"])
    
    frequency = {}
    for item in submission_list:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    for i in frequency:
        csv_writer.writerow([i,frequency[i]])
        
    data_file.close()
    data = pd.read_csv(curDir+'atcoder.csv',parse_dates=['Date'])
    data = data.set_index('Date')
    calplot.calplot(data['Submissions'],daylabels='MTWTFSS',dayticks=[0, 2, 4, 6],yearlabel_kws={'fontsize':18})
    plt.show()
    saveHandle()
        

@cli.command('download', short_help='Get all of your Submisssions From AtCoder locally!!')
def download():  
    global pathDir
    global scrappedTill
    global curDir
    global handle
    r = requests.get('https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user='+handle+'&from_second=0')
    handleVeri=r.json()
    if handleVeri==[]:
        click.secho(f'Handle {handle} not found 😒',bold=True,fg='red')
        return
    try:
        isExist=os.path.exists(pathDir)
        if not isExist:
            os.makedirs(pathDir)
        pageNo=1
        urlQuery='?f.Task=&f.LanguageName=&f.Status=AC&f.User='
        url="https://atcoder.jp/contests/archive?page="+str(pageNo)
        pageHtmlText=requests.get(url).text
        pageSoup=BeautifulSoup(pageHtmlText,'lxml')
        pagination=pageSoup.find('ul','pagination')
        totalPages=int(pagination.find_all('li')[-1].a.text)
        contestno=0
        while pageNo<=totalPages:
            url="https://atcoder.jp/contests/archive?page="+str(pageNo)
            click.secho(f'Parsing Page Number ⛏ {pageNo}:',bold=True)
            htmlText=requests.get(url).text    
            soup=BeautifulSoup(htmlText,'lxml')
            table=soup.find('table')
            for row in table.find_all('tr'):
                columns=row.find_all('td')
                if columns!=[]:
                    if contestno<scrappedTill:
                        contestno+=1
                        continue
                    contestDir=columns[1].a.text
                    subPageUrl='https://atcoder.jp'+columns[1].a['href']+'/submissions'+urlQuery+handle
                    subHtmlText=requests.get(subPageUrl).text
                    subSoup=BeautifulSoup(subHtmlText,'lxml')
                    subTable=subSoup.find('table')
                    if subTable==None:
                        contestno+=1
                        click.secho(f'No problems solved in contest {contestDir} 🤐')
                        continue
                    for subRow in subTable.find_all('tr'):
                        subColumns=subRow.find_all('td')    
                        if(subColumns!=[]):
                            solutionIdx=subColumns[1].a.text[0]
                            solutionUrl='https://atcoder.jp'+subColumns[9].a['href']
                            solHtmlText=requests.get(solutionUrl).text
                            solSoup=BeautifulSoup(solHtmlText,'lxml')
                            solution=solSoup.find('pre').text
                            solTable=solSoup.find('table',class_='table')
                            lang =solTable.find_all('tr')[3].find('td').text
                            langExtension=getLang(lang)
                            solPath=pathDir+contestDir
                            pathExist=os.path.exists(solPath)
                            if not pathExist:
                                os.makedirs(solPath)       
                            myfile = Path(solPath+"/"+solutionIdx+"."+langExtension)
                            myfile.touch(exist_ok=True)
                            f = open(myfile,'w')    
                            f.writelines(solution)
                            f.close()
                    click.secho(f'{contestDir} Solutions Downloaded ✅',fg='green')
                    scrappedTill=contestno+1
                    contestno+=1

            pageNo+=1

        click.secho("🎊 Task Completed 🎊",bold='True',fg='bright_green')
    except Exception as e:
        with open(curDir+'AtcoderCount.txt','w') as f:
            f.write(str(scrappedTill))    
        saveHandle()  
        click.secho(e)
    finally:
        scrappedTill=contestno
        with open(curDir+'AtcoderCount.txt','w') as f:
            f.write(str(scrappedTill)) 
        saveHandle()