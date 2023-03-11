import requests
from bs4 import BeautifulSoup
from statistics import Fight,Strike,statistics

from flask import Flask,request
import pandas as pd
from pymodm import connect

connect('mongodb://localhost:27017/ufcdatabase')

app = Flask(__name__)
@app.route("/sendtoserver")
def savetodata(data):
    data.save()
    return "hello world"
@app.route("/<fightername>",methods =['GET','POST'])
def home(fightername):

    URL = "https://www.ufc.com/athlete/"+fightername+"#athlete-record"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content,'html5lib')
    cards = soup.findAll('div', attrs={'class': 'c-card-event--athlete-results__info'})
    fights_data = fights_info(cards)
    wins_target = soup.findAll('div', attrs={'class': 'stats-records-inner'})
    generals_table = generals(soup)
    wins_target_table = wins(wins_target)
    takedowns_tables = takedowns(soup)
    strikes = strikes_la(wins_target, soup)

    return [wins_target_table[0],takedowns_tables[0],strikes[0],strikes[1],strikes[2],fights_data,generals_table]
def wins(wins_target) :
    wins_by_method = wins_target[7].find('div').findAll('div')[0].findChildren()
    tko  = int(wins_by_method[2].text.split(" ")[0])
    dec  = int(wins_by_method[5].text.split(" ")[0])
    sub = int(wins_by_method[8].text.split(" ")[0])
    wins_df = pd.DataFrame.from_records([{"ko":tko,"dec":dec,"sub":sub}])
    return [{"ko":tko,"dec":dec,"sub":sub}]

def strikes_la(wins_target,soup):
    #strikes by position
    str_position = wins_target[5].find('div').findAll('div')[0].findChildren()
    standing  = int(str_position[2].text.split(" ")[0])
    clinch = int(str_position[5].text.split(" ")[0])
    ground = int(str_position[8].text.split(" ")[0])
    #strikes by target
    head = int(soup.find('text',attrs={'id':"e-stat-body_x5F__x5F_head_value"}).text)
    body = int(soup.find('text',attrs={'id':"e-stat-body_x5F__x5F_body_value"}).text)
    leg = int(soup.find('text',attrs={'id':"e-stat-body_x5F__x5F_leg_value"}).text)
    #strikes landed attempted
    strikes_landed = int(soup.findAll('dd',attrs={'class':'c-overlap__stats-value'})[0].text)
    strikes_attempted = int(soup.findAll('dd',attrs={'class':'c-overlap__stats-value'})[1].text)
    strikes_position_df = pd.DataFrame.from_records([{"standing":standing,"clinch":clinch,"ground":ground}])
    strikes_target_df = pd.DataFrame.from_records([{"head":head,"body":body,"leg":leg}])

    return  [{"standing":standing,"clinch":clinch,"ground":ground},{"head":head,"body":body,"leg":leg}
        ,{"strikr_landed":strikes_landed,"strike_att":strikes_attempted}]

def takedowns(soup):
    #takedowns
    takedown_landed = soup.findAll('dd',attrs={'class':'c-overlap__stats-value'})[2].text
    takedown_attempted = int(soup.findAll('dd',attrs={'class':'c-overlap__stats-value'})[3].text)
    return [{"attempted":takedown_attempted,"landed":takedown_landed}]

def generals(soup) :
    #generals
    nickname = soup.find('p',attrs={'class':'hero-profile__nickname'}).getText()
    profile_photo = soup.find('img',attrs={'class':'hero-profile__image'})['src']
    name = soup.find('h1',attrs={'class':'hero-profile__name'}).text
    division = soup.find('p',attrs={'class':'hero-profile__division-title'}).text
    active_ranking = soup.findAll('p',attrs={'class':'hero-profile__tag'})
    active = active_ranking[1].text
    ranking = active_ranking[0].text.strip().split(" ")[0]
    return [nickname,name,division,active,ranking,profile_photo]

def fights_info(cards) :
    fights = []
    for dat in cards :
        divs = dat.findAll('div')
        subdivs = divs[1].findAll('div')
        round = subdivs[0].findAll("div")
        timediv = subdivs[3].findAll("div")
        methoddiv = subdivs[-1]
        vs = dat.h3.text
        datefight = divs[0].time.text
        round = int(round[1].text)
        timefight = timediv[1].text
        method = methoddiv.text
        fights.append({"vs":vs,"datefight":datefight,"round":round
                          ,"timefight":timefight,"method":method})
    return fights


if __name__ == "__main__":
    app.run(debug=True)

