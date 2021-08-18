# cd FastAPI_naraz
# uvicorn main:app --reload

# from typing import Optional
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from datetime import datetime, timedelta
# from bs4 import BeautifulSoup
# import requests

# def search(item_name: str, period: Optional[int] = 1):
#     searchdate = period
#     now = datetime.now()
#     yest = now - timedelta(days=searchdate)

#     # keyword_key = [item_name]
#     keyword_key = item_name.split(",")
#     keyword_ing = [i.encode('EUC-KR') for i in keyword_key]
#     keyword_value = [str(j).replace("\\x", "%").strip("b'").replace(" ", "+") for j in keyword_ing]
#     keyword = dict(zip(keyword_key, keyword_value))       

#     lst_a = {}
#     for key, value in keyword.items():
#         url_a = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?searchType=1&bidSearchType=1&taskClCds=5&bidNm={0}&searchDtType=1&".format(value)
#         url_b = "fromBidDt=2021%2F{0}%2F{1}&toBidDt=2021%2F{2}%2F{3}&fromOpenBidDt=&toOpenBidDt=&radOrgan=1&instNm=&instSearchRangeType=&refNo=&area=&areaNm=\
#             &industry=&industryCd=&budget=&budgetCompare=UP&detailPrdnmNo=&detailPrdnm=&procmntReqNo=&intbidYn=&regYn=Y&recordCountPerPage=50".format(yest.month, yest.day, now.month, now.day)
#         url = url_a + url_b
#         res = requests.get(url)
#         res.raise_for_status()
#         lst_b = []
#         lst_a[key] = lst_b
#         soup = BeautifulSoup(res.text, "lxml")
#         lst1 = soup.find_all("tr", attrs={"onmouseover":"this.className='on'"})
#         for each in lst1 :
#             row = each.find_all("div")
#             row3 = row[3].text
#             row4 = row[4].text
#             row5 = row[5].text
#             row6 = (row[6].text.replace('(',''))[:4]
#             row7 = row[7].text
#             lst_b.append([row3, row4, row5, row6, row7])
#     return lst_a

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# @app.get("/items/{id}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})




@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})

# @app.post("/search/result", response_class=HTMLResponse)
# async def handle_form(request: Request, item_name: str = Form(...), period: int = Form(...)):
#     return templates.TemplateResponse("item2.html", {"request": request, "lst_a": search(item_name, period)})


