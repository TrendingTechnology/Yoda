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

# handle=input("Enter your CodeForces Handle: ")
handle=""
# langExtension=input("Enter your Language Extension: ")
langExtension="cpp"
# pathDir=input("Enter your path you wnat to keep Solutions: ")
pathDir='/home/nm/CP-Solutions/'
pathDir+='CodeForces/'
curDir='/home/nm/Code/Statify/'
scrappedTill=0
def getHandle():
    global handle
    global pathDir
    global scrappedTill
    global curDir
    f=open(curDir+'EndpointCount.txt','a')
    f.close()
    with open(curDir+'EndpointCount.txt') as f:
        somethingInteresting=f.readlines()
        if somethingInteresting!=[]:
            scrappedTill=(int(somethingInteresting[0]))
    f=open(curDir+'handleCf.txt','a')
    f.close()
    with open(curDir+'handleCf.txt') as f:
        somethingInteresting=f.readlines()
        if somethingInteresting==[]:
            return
        handle=str(somethingInteresting[0])
    pathDir='/home/nm/CP-Solutions/CodeForces/'+handle+'/'
    
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
    pathDir='/home/nm/CP-Solutions/CodeForces/'+handle+'/'

def saveHandle():
    global handle
    global curDir
    with open(curDir+'handleCf.txt','w') as f:
        f.write(handle)
    

def getLang(lang):
    global langExtension
    if('GNU' in lang or "++" in lang or "GCC" in lang or "Clang" in lang):
        langExtension="cpp"
    elif "C#" in lang:
        langExtension="cs"
    elif 'Go' in lang:
        langExtension='go'
    elif "Kotlin" in lang:
        langExtension="kt"
    elif "Py" in lang:
        langExtension='py'
    elif 'JavaScript'  or 'js' in lang:
        langExtension='js'
    elif  "Java" in lang:
        langExtension='java'
    elif 'Scala' in lang:
        langExtension='scala'
    elif 'Ruby' in lang:
        langExtension='rb'
    elif 'Rust' in lang: 
        langExtension='rs'
    elif 'D' in lang:
        langExtension='d'
    else:
        langExtension='txt'
    return langExtension

@click.group()
def cli():
    """👋 Get your Data from CodeForces!!🚀"""
    getHandle() 
    han=input("Enter your Prestigious CodeForces handle: ")
    changeHandle(han)
@cli.command('graph', short_help='Get your Submisssion Heatmap!!')
def graph():
    global handle
    global curDir
    r = requests.get('https://codeforces.com/api/user.status?handle='+handle)
    jsondata = r.json()
    if jsondata['status']=='OK':
        data_file = open(curDir+'codeforces.csv', 'w')
        csv_writer = csv.writer(data_file)
        csv_writer.writerow(["Date","Submissions"])
        submission_list = []
        cnt  = set()
        for data in jsondata["result"]:
            timestamp = datetime.datetime.utcfromtimestamp(data["creationTimeSeconds"]).date()
            probem_name = f'{data["problem"]["contestId"]}{data["problem"]["index"]}'
            if(data["verdict"]=="OK" and probem_name not in cnt):
                date = timestamp
                cnt.add(probem_name)
                submission_list.append(date)

        frequency = {}
        for item in submission_list:
            if item in frequency:
                frequency[item] += 1
            else:
                frequency[item] = 1

        for i in frequency:
            csv_writer.writerow([i,frequency[i]])
            
        data_file.close()
        data = pd.read_csv(curDir+'codeforces.csv',parse_dates=['Date'])
        data = data.set_index('Date')
        calplot.calplot(data['Submissions'],daylabels='MTWTFSS',dayticks=[0, 2, 4, 6],yearlabel_kws={'fontsize':18})
        plt.show()
        saveHandle()
    else:
        click.secho(jsondata['comment'],bold=True,fg='red')

@cli.command('download', short_help='Get all of your Submisssions From CodeForces locally!!')
def download():
    global scrappedTill
    global handle
    global pathDir
    global curDir
    try:
        isExist=os.path.exists(pathDir)
        if not isExist:
            os.makedirs(pathDir)
        
        url='https://codeforces.com/api/user.status?handle='+handle
        r=requests.get(url).json()
        if r['status']=='OK':
            problemId=set()
            solId=[]
            for result in r['result']:
                if result['verdict']=='OK':
                    if 'contestId' not in result['problem'] or 'index' not in result['problem']:
                        continue
                    if str(result['problem']['contestId'])+result['problem']['index'] not in problemId:
                        problemId.add(str(result['problem']['contestId'])+result['problem']['index'])
                        solId.append([result['id'],result['problem']['contestId'],result['programmingLanguage']])
            curCount=0
            for sol in solId:
                if curCount<scrappedTill:
                    curCount+=1
                    continue
                if sol[1]>=10000:
                    scrappedTill+=1
                    curCount+=1
                    continue
                problemUrl='https://codeforces.com/contest/'+str(sol[1])+'/submission/'+str(sol[0])
                lang=sol[2]
                langExtension=getLang(lang)
                subHtmlText=requests.get(problemUrl).text
                subSoup=BeautifulSoup(subHtmlText,'lxml')
                subTable=subSoup.find('table')
                problemIdx=""
                for subRow in subTable.find_all('tr'):
                    subColumns=subRow.find_all('td')
                    if subColumns!=[]:
                        problemIdx=subColumns[2].a.text.strip()
                solution=subSoup.find('pre',id="program-source-text").text
                contestDir=pathDir+str(sol[1])
                pathExist=os.path.exists(contestDir)
                if not pathExist:
                    os.makedirs(contestDir)   
                till=-1
                if problemIdx[-1].isnumeric():
                    till=-2    
                myfile = Path(contestDir+"/"+problemIdx[till:]+"."+langExtension)
                myfile.touch(exist_ok=True)
                f = open(myfile,'w')    
                f.writelines(solution)
                f.close()
                click.secho(f'{problemIdx} of contest Id {sol[1]} downloaded ✅',fg='green')
                scrappedTill+=1
                curCount+=1
            click.secho("🎊 Task Completed 🎊",fg='bright_green')
        else:
            click.secho(r['comment'],fg='red')
    except Exception as e:
        with open(curDir+'EndpointCount.txt','w') as f:
            f.write(str(scrappedTill)) 
        saveHandle()     
        click.secho(f'Restart the command after 5-10 minutes Codeforces blocked you temporarily because of too many requests 😿 ',fg='red')
    finally:
        with open(curDir+'EndpointCount.txt','w') as f:
            f.write(str(scrappedTill)) 
        saveHandle()