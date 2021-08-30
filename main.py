# cd FastAPI_naraz
# uvicorn main:app --reload

from typing import Optional
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re

def search_gg(item_name: str, period: Optional[int] = 1):
    searchdate = period
    now = datetime.now()
    yest = now - timedelta(days=searchdate)

    # keyword_key = [item_name]
    keyword_key = item_name.split(",")
    keyword_ing = [(i.encode('EUC-KR')) for i in keyword_key]
    keyword_value = [str(j).replace("\\x", "%").strip("b'").replace(" ", "+") for j in keyword_ing]
    keyword = dict(zip(keyword_key, keyword_value))       

    lst_gg = {}
    for key, value in keyword.items():
        url_a = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?searchType=1&bidSearchType=1&taskClCds=5&bidNm={0}&searchDtType=1&".format(value)
        url_b = "fromBidDt=2021%2F{0}%2F{1}&toBidDt=2021%2F{2}%2F{3}&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&instSearchRangeType=&refNo=&area=&areaNm=\
            &industry=&industryCd=&budget=&budgetCompare=UP&detailPrdnmNo=&detailPrdnm=&procmntReqNo=&intbidYn=&regYn=Y&recordCountPerPage=50".format(yest.month, yest.day, now.month, now.day)
        url = url_a + url_b
        res = requests.get(url)
        res.raise_for_status()
        lst_b = []
        lst_gg[key] = lst_b
        soup = BeautifulSoup(res.text, "lxml")
        lst1 = soup.find_all("tr", attrs={"onmouseover":"this.className='on'"})
        for each in lst1 :
            sub_url = each.find("a")["href"] # 검색결과로 들어가는 각 링크 가져오기
            res2 = requests.get(sub_url)
            res2.raise_for_status()
            soup2 = BeautifulSoup(res2.text, "lxml")
            money = {"money": soup2.find("th", text="배정예산").next_sibling.next_sibling.text.strip()}

            row = each.find_all("div")
            name = {"name": row[3].text}
            row4 = row[4].text
            gov = {"gov": row[5].text}
            row6 = (row[6].text.replace('(',''))[:4]
            deadline = {"deadline": row[7].text}

            lst_b.append([name, gov, deadline, money])
            
    return lst_gg

def search_sj(item_name: str, period: Optional[int] = 1):
    searchdate = period
    now = datetime.now()
    yest = now - timedelta(days=searchdate)
    keyword_key = item_name.split(",")
    keyword_ing = [(i.encode('EUC-KR')) for i in keyword_key]
    keyword_value = [str(j).replace("\\x", "%").strip("b'").replace(" ", "+") for j in keyword_ing]
    keyword = dict(zip(keyword_key, keyword_value))

    lst_sj = {}
    for key, value in keyword.items():
        url = "http://www.g2b.go.kr:8081/ep/preparation/prestd/preStdPublishList.do?dminstCd=&fromRcptDt=2021%2F{1}%2F{2}&instCl=2&instNm=&orderbyItem=1&prodNm={0}\
            &recordCountPerPage=50&searchDetailPrdnm=&searchDetailPrdnmNo=&searchType=1&supplierLoginYn=N&swbizTgYn=&taskClCd=5&taskClCds=5&toRcptDt=2021%2F{3}%2F{4}&currentPageNo=1".format(value, yest.month, yest.day, now.month, now.day)
        res = requests.get(url)
        res.raise_for_status()
      
        lst_b = []
        lst_sj[key] = lst_b
        soup = BeautifulSoup(res.text, "lxml")
        lst1 = soup.find_all("tr", attrs={"onmouseover":"this.className='on'"}) 

        for each in lst1 :
            row = each.find_all("div") # 
            name = {"name": row[3].text.strip()}
            gov = {"gov": row[4].text.strip()}

            sub_url = "https://www.g2b.go.kr:8143/ep/preparation/prestd/preStdDtl.do?preStdRegNo={0}".format(row[1].text.strip())
            res2 = requests.get(sub_url)
            res2.raise_for_status()
            soup2 = BeautifulSoup(res2.text, "lxml")

            deadline = {"deadline": soup2.find("th", text="의견등록마감일시").next_sibling.next_sibling.text.strip()}
        
            s = soup2.find("th", text="배정예산액").next_sibling.next_sibling.text.strip()
            ss = re.findall('\\d+', s)
            sss = "".join(ss)
            money = {"money": "{:,}".format(int(sss))}
            lst_b.append([name, gov, deadline, money])

    return lst_sj



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item3.html", {"request": request})

# 공고 검색
# 키워드 : item_name / 검색기간 : period
@app.get("/gg/{item_name}/{period}")
async def read_item(item_name: str = "", period: int = 1):
    return search_gg(item_name, period)


# 사전규격 검색
# 키워드 : item_name / 검색기간 : period
@app.get("/sj/{item_name}/{period}")
async def read_item(item_name: str = "", period: int = 1):
    return search_sj(item_name, period)