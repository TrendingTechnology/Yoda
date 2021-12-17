from bs4 import BeautifulSoup
import requests
import os
import json
from pathlib import Path
from datetime import datetime 
import csv
import pandas as pd
import numpy as np
import datetime 
import calplot
import matplotlib.pyplot as plt
import click
# handle=input("Enter your CodeForces Handle: ")
final_array=[]
handle=''
# langExtension=input("Enter your Language Extension: ")
langExtension="cpp"
# pathDir=input("Enter your path you wnat to keep Solutions: ")
pathDir=''
curDir='/home/nm/Code/Statify/'
def getHandle():
    global handle
    global pathDir
    global final_array
    global curDir
    f=open(curDir+'handle.txt','a')
    f.close()
    with open(curDir+'handle.txt') as f:
        somethingInteresting=f.readlines()
        if somethingInteresting==[]:
            return
        handle=str(somethingInteresting[0])
    pathDir='/home/nm/CP-Solutions/CodeChef/'+handle+'/'
    with open(curDir+'DataBackup.txt') as f:
        somethingInteresting=f.readlines()
        if(somethingInteresting!=[]):
            for i in somethingInteresting[0].split(','):
                if i.split('@') not in final_array:
                    final_array.append((i.split('@')))

def changeHandle(han):
    global handle
    global final_array
    global pathDir
    if handle==han:
        saveHandle()
        return
    handle=han
    saveHandle()
    final_array=[]
    pathDir='/home/nm/CP-Solutions/CodeChef/'+handle+'/'

def saveHandle():
    global handle
    global curDir
    with open(curDir+'handle.txt','w') as f:
        f.write(handle)



def scrape():
    global final_array
    global handle
    global curDir
    url="https://www.codechef.com/users/"+handle+"/"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    contests=(soup.find_all('div',class_='content')[3].find('article').find_all('p'))
    for contest in contests:
        contestDir=(contest.strong.text)[:-1]
        contestBool=contestDir
        if(contestDir=='Practice'):
            contestBool=""
        click.secho(f'⛏ Scanning contest {contestDir} :')
        problems = contest.find_all('a', rel="nofollow")
        for problem in problems:
            click.secho(f'⌛ Scanning your solution to problem {problem.text}:')
            problem_status_url = "https://www.codechef.com/"+contestBool+"/status/"+problem.text+","+handle
            problem_status_html_text = requests.get(problem_status_url).text
            problem_soup = BeautifulSoup(problem_status_html_text,'lxml')
            problem = problem_soup.find("table", class_="dataTable")
            if problem==None:
                continue
            sub_url = ""
            date_time_obj=datetime.datetime.min 
            imgUrl="https://cdn.codechef.com/misc/tick-icon.gif"
            for row in problem.find_all('tr'):
                columns = row.find_all('td')
                if(columns!=[]):
                    if(columns[3].find("span").find('img')['src']==imgUrl):
                        if (str(columns[7].find('a'))=='<a class="disabled">View</a>'):
                            click.secho('Contest Data removed From CodeChef 😿',fg='yellow')
                            continue
                        sub_url = columns[7].a["href"]
                        if(columns[1].text==None):
                            continue
                        date_time=columns[1].text
                        if 'hours ago' in date_time:
                            continue
                        date_time_obj = datetime.datetime.strptime(date_time, '%I:%M %p %d/%m/%y')       
                        break
            if(sub_url=="" or date_time_obj==datetime.datetime.min):
                continue
            if ([sub_url,date_time_obj,contestDir] not in final_array):
                final_array.append([sub_url,date_time_obj,contestDir])
    
    with open(curDir+'DataBackup.txt','w') as f:
        s=""
        for x in final_array:
            s+=str(x[0])+'@'+str(x[1])+'@'+str(x[2])
            s+=','
        s=s[:-1]
        f.write(s) 


@click.group()
def cli():
    """👋 Get your Data from CodeChef!!🚀"""
    getHandle() 
    han=input("Enter your Prestigious CodeChef handle: ")
    changeHandle(han)

@cli.command('graph', short_help='Get your Submisssion Heatmap!!')
def graph():
    global final_array
    global curDir
    global handle
    if final_array==[]:
        scrape()
    data_file = open(curDir+'codechef.csv', 'w')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(["Date","Submissions"])
    frequency = {}
    for dummy1,item,dummy2 in final_array:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    for i in frequency:
        csv_writer.writerow([i,frequency[i]])   
    data_file.close()
    data = pd.read_csv(curDir+'codechef.csv',parse_dates=['Date'])
    data = data.set_index('Date')
    calplot.calplot(data['Submissions'],daylabels='MTWTFSS',dayticks=[0, 2, 4, 6],yearlabel_kws={'fontsize':18})
    plt.show()
    saveHandle()



@cli.command('download', short_help='Get all of your Submisssions From CodeChef locally!!')
def download():  
    global final_array
    global curDir
    global pathDir
    isExist=os.path.exists(pathDir)
    if not isExist:
        os.makedirs(pathDir)
    if final_array==[]:
        scrape()
    for sub_url,date_time,contestDir in final_array:
        the_end_url = "https://www.codechef.com"+sub_url
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}
        html_text_end=requests.get(the_end_url,headers=headers).text
        soup_end=BeautifulSoup(html_text_end,'lxml')

        script=soup_end.find_all('script')[45].text.strip()[16:-1]

        data=json.loads(script)
        langExtension=data['data']['languageExtension']
        solution=data["data"]['plaintext']
        probName=data["data"]["problemCode"]
        solPath=pathDir+contestDir+'/'+probName
        pathExist=os.path.exists(solPath)
        if not pathExist:
            os.makedirs(solPath)  
             
        myfile = Path(solPath+"/"+probName+"."+langExtension)
        myfile.touch(exist_ok=True)
        f = open(myfile,'w')    
        f.writelines(solution)
        f.close()
        click.secho(f'Solution to Problem {probName} downloaded !! ✅',fg='green')
    click.secho("🎊 Task Completed 🎊",fg='bright_green',bold=True)
    saveHandle()

