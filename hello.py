from selenium import webdriver
import time
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask import request
# start web browser
import requests
browser = webdriver.Firefox()


baseUrl = "https://www.universitego.com/bilgisayar-muhendisligi-2020-taban-puanlari-ve-basari-siralamalari/"
source = requests.get(baseUrl).text
bolumListesi = []  # bölümler

author = "Serkan Özcan"
BolumAdı = "Bilgisayar Mühendisliği"
browser.get(baseUrl)

time.sleep(2)

soup = BeautifulSoup(source, 'html.parser')
bolumler = soup.find_all("tr")

for bolum in bolumler:
    bolum_td = bolum.find_all("td")
    if(len(bolum_td) == 6):
        bolum = {}
        bolum['universite'] = (bolum_td[0].string)
        bolum['name'] = (bolum_td[1].string)
        bolum['tür'] = (bolum_td[2].string)
        bolum['kontenjan'] = (bolum_td[3].string)
        bolum['tabanPuan'] = (bolum_td[4].string)
        bolum['basariSirasi'] = (bolum_td[5].string)
        bolum['sans'] = " "
        bolumListesi.append(bolum)
        bolum = {}


bolumListesi.pop(0)
app = Flask(__name__)


browser.close()


@app.route('/')
def index(bolumListesi=bolumListesi):
    return render_template('index.html', **locals())


@app.route('/sonuc', methods=['POST'])
def handle_data():
    puan = request.form['puan']
    sansliListe = []
    for b in bolumListesi:
        print(b['tabanPuan'])
        if(b['tabanPuan'] == "Dolmadı"):
            sansliListe.append(b)
            b['sans'] = "🧐"
        else:
            b['tabanPuan'] = ((b['tabanPuan'].replace(",", ".")))
            if(b['tabanPuan'] != "Dolmadı" and (float(puan) < float(b['tabanPuan']))):
                b['sans'] = "😔"
                sansliListe.append(b)
            elif(b['tabanPuan'] != "Dolmadı" and (float(puan) >= float(b['tabanPuan']))):
                b['sans'] = "🥳"
                sansliListe.append(b)

    return render_template('sonuc.html', puan=puan, bolumListesi=sansliListe)


app.run(debug=True)
print(puan)
BeautifulSoup
