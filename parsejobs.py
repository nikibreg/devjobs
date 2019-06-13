from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import asyncio 

async def parseMyJobsGE(statementsHTML):
    statements = []
    for statementHTML in statementsHTML:
        soup = BeautifulSoup(statementHTML.html, "html.parser")
        # statement data structure
        statements.append({
            "site": "myjobs.ge",
            "title": soup.find("h4").text,
            "organization": soup.find("span", {"itemprop":"name"}).text,
            "description": soup.find("p", {"class":"block"}).text,
            "location": soup.find("span", {"itemprop":"addressLocality"}).text,
            "salary": soup.find("span", {"itemprop": "baseSalary"}).text if soup.find("span", {"itemprop": "baseSalary"}) else "შეთანხმებით",
            "href": soup.select_one("h4 a").get('href'),
            "date": soup.find("p", {"class":"date"}).text
        })
    return statements


def safeField(field, obj, safevalue):
    return obj[field] if field else safevalue


async def parseJobsGE(statementsHTML):
    statements = []
    for statementHTML in statementsHTML:
        soup = BeautifulSoup(statementHTML.html, "html.parser")
        # statement data structure
        statement = {
            "site": "jobs.ge",
            "title": soup.select_one(selector="td:nth-child(2) a").text,
            "organization": soup.select_one(selector="td:nth-child(4) a").text if soup.select_one(selector="td:nth-child(4) a") else "კომპანია",
            # "description": soup.find("p", {"class":"block"}).text,
            # "location": soup.find("span", {"itemprop":"addressLocality"}).text,
            # "salary": soup.find("span", {"itemprop": "baseSalary"}).text if soup.find("span", {"itemprop": "baseSalary"}) else "შეთანხმებით",
            # "href": soup.select_one("h4 a").get('href'),
            "description": "დამატებითი ინფორმაციისთვის დაგვიკავშირდით",
            "location": "თბილისი",
            "salary": "შეთანხმებით",
            "href": "http://jobs.ge/" + soup.select_one("td:nth-child(2) a").get('href'),
            "date": truncateDate(soup.select_one(selector="td:nth-child(5)").text) + " - " + truncateDate(soup.select_one(selector="td:nth-child(6)").text),
        }
        
            # "title": soup.find("h4").text,
        #     "organization": soup.find("span", {"itemprop":"name"}}).text,
        #     "description": soup.find("p", {"class":"block"}).text,
        #     "location": soup.find("span", {"itemprop":"addressLocality"}).text,
        #     "salary": soup.find("span", {"itemprop": "baseSalary"}).text if soup.find("span", {"itemprop": "baseSalary"}) else "შეთანხმებით",
        #     "href": soup.select_one("h4 a").get('href'),
        #     "date": soup.find("p", {"class":"date"}).text
        # })
        statements.append(statement)
    return statements

def truncateDate(dateString):
    return dateString[0:6]+"."




websites = [
    {
        "name":"myjobs.ge",
        "url": "https://www.myjobs.ge/ka/?cat_id=1&page=1&sort=6",
        "cb": parseMyJobsGE,
        "statement-selector": "div.statement" 
    },
    {
        "name":"jobs.ge",
        "url": "https://www.jobs.ge/?page=1&q=&cid=6&lid=&jid=",
        "cb": parseJobsGE,
        "statement-selector": "#wrapper > div.regularEntries > table > tbody > tr:has(td)"
    },
]

async def parseAll():
    statements = []
    for website in websites:
        session = AsyncHTMLSession() 
        # gets html
        response = await session.get(website['url'])
        # renders html that's generated by javascript
        await response.html.arender()
        # html elements
        statementsHTML = response.html.find(selector=website['statement-selector'])
        # we store actual statements here
        statements.extend(await website['cb'](statementsHTML))
    return statements

async def parse():
    return await parseAll()