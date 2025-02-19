import requests
from bs4 import BeautifulSoup
import re
import asyncio
import pywhatkit
import datetime
import time
import sys
import os
import functools
Global_flag=False
hour=int(time.strftime('%H'))
minut=int(time.strftime('%M'))
async def wa(f_L):
    global Global_flag
    try:
    # Get the current time
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute + 1  # Add 1 minute to the current time

        # Ensure the minute doesn't exceed 59
        if current_minute == 60:
            current_minute = 0
            current_hour += 1
            if current_hour == 24:
                current_hour = 0  # Reset hour if it exceeds 24

        # sending message to receiver using pywhatkit
        pywhatkit.sendwhatmsg("+918850410674", 
                                f"{f_L}", 
                                current_hour, 
                                current_minute)
        print("Successfully Sent!")

    except Exception as e:
        # handling exception and printing error message
        print("An Unexpected Error!", e)
        Global_flag=True

@functools.cache
def test(f,flag=False):
  try:
    if flag:
        print(f,flag)
        r=requests.get(f"https://www.moneycontrol.com/indian-indices/{f}",timeout=400)
        soup=BeautifulSoup(r.text,'html.parser')
        find=soup.find_all('div',id="sp_ch_prch") 
        text=find[0].text
        match = re.search(r"(-?\d+\.\d+)%", text)
        print(match.group(1))        
        return(match.group(1))
    else:
        r=requests.get(f"https://www.moneycontrol.com/india/stockpricequote/miscellaneous/{f}",timeout=400)
        soup=BeautifulSoup(r.text,'html.parser')
        find=soup.find_all('div',id="nsechange") 
        text=find[0].text
        match = re.search(r"(-?\d+\.\d+)%", text)
        print(match.group(1))   
        return(match.group(1))
  except Exception as e:
     asyncio.run(wa(e))
     return 1


async def test2():
    res=""""""
    lis=['TATSI21428','NIFTY-50-9.html','nifty-it-19.html','sensex-4.html','NIFTY-BANK-23.html','nifty-smallcap-100-53.html','NIFTY-Midcap-100-27.html','TATAG21401']
    for i in lis:
      if i.find('.html')>-1: 
       print(i.find('.html'))
       if float(test(i,True)) < -0.99:
          res+="INDEX: "+i+': '+ test(i,True)+'\n'
      else:
        if float(test(i,False))<-0.01:
          res+="COMODITY: "+i+': '+ test(i,False)+'\n'
    await wa(res)
    
async def main():
   task=asyncio.create_task(test2())
   res=await task
   print(res)
   
asyncio.run(main())

if Global_flag :
    time.sleep(20)
    script_name = sys.argv[0]
    os.system(f"python {script_name}")