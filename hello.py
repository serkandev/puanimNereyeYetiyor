import time
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests

# sıralamaya göre seçeneği lazım bir de

baseUrl = "https://tercihgo.com/2020-4-yillik-bolumlerin-taban-puanlari-ve-basari-siralamalari"
u_url = "https://tercihgo.com/2020-universite-bolumlerin-taban-puanlari-ve-basari-siralamalari"

def getJobList(bolumlerUrl):
    JobSource = requests.get(bolumlerUrl).text
    JobList = []
    soup = BeautifulSoup(JobSource, 'html.parser')
    JobNames = soup.find_all("a", {'style': "color: #ff6600;"})
    for job in JobNames:
        j = {}
        j['name'] = ((job).text).replace('2020 Taban Puanları', "")
        j['link'] = job.get('href')
        JobList.append(j)
        j = {}
    print(JobList)
    return(JobList)


jobList = (getJobList(baseUrl))
u_list = getJobList(u_url)


app = Flask(__name__)


@app.route('/')
def index(joblist=jobList):
    return render_template('index.html', **locals())

@app.route("/universiteler")
def universiteler(u_list = u_list):
    return render_template("universiteler.html", **locals())

@app.route('/sonuc', methods=['POST'])
def handle_data():
    puan = float(request.form['puan'])
    bolum = request.form['bolum']
    source = requests.get(bolum).text
    soup = BeautifulSoup(source, 'html.parser')
    bolumler = soup.find_all("tr")
    bolumListesi = []

    for info in bolumler:
        bolum_data = info.find_all("td")
        if(len(bolum_data) == 6):
            bolum = {}
            bolum['univercity'] = (bolum_data[0]).string
            bolum['job'] = bolum_data[1].string
            bolum['type'] = bolum_data[2].string
            bolum["quota"] = bolum_data[3].string
            bolum['base_score'] = bolum_data[4].string
            bolum['placement'] = bolum_data[5].string
            bolum['luck'] = ""
            bolum['bg'] = ""
            bolumListesi.append(bolum)
            bolum = {}
    try: # bazıları boş liste döndürüyor üniversiteye göre aramada
        bolumListesi.pop(0) 
    except:
        print("Exception handled.")
    sansliListe = []

    for b in bolumListesi:
        if(b['base_score'] == "Dolmadı"):
            sansliListe.append(b)
            b['luck'] = "🥶"
            b['bg'] = "bg-secondary"
        elif(b['base_score'] == "---"):
            sansliListe.append(b)
            b['luck'] = "🥶"
            b['bg'] = "bg-secondary"
        else:
            b['base_score'] = float((b['base_score'].replace(",", ".")))
            if(b['base_score'] != "Dolmadı" and (puan < b['base_score'])):
                diffrence = b['base_score'] - puan
                if(diffrence <= 25):
                    b['luck'] = "🤔"
                    b['bg'] = "bg-primary"
                else:
                    b['luck'] = "🥺"
                    b['bg'] = "bg-danger"
                sansliListe.append(b)
            elif(b['base_score'] != "Dolmadı" and puan >= b['base_score']):
                b['luck'] = "🥳"
                b['bg'] = "bg-success"
                sansliListe.append(b)

    return render_template('sonuc.html', puan=puan, bolumListesi=sansliListe)


app.run(debug=True)
