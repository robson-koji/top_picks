
import os, sys, time, django

import requests
import datetime
import json
from bs4 import  BeautifulSoup

def get_home():
    """ retorna generator de empresas """

    HOME_URL = 'https://ondeinvestir.lopesfilho.com.br/embed/carteiras/carteira-top-picks/'
    sess = requests.Session()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=8aq9a87p9rh4apeind522drho1; ARRAffinity=c83c2289f9a097e5bb3a55d79ea33cdbab1c8d9fa07af5e8cc2d1720095ca46b; __utma=262044560.214949217.1575315259.1578334313.1580317431.5; __utmc=262044560; __utmz=262044560.1580317431.5.5.utmcsr=easynvest.com.br|utmccn=(referral)|utmcmd=referral|utmcct=/configuracoes/onde-investir; __utmb=262044560.23.9.1580318898853',
        'Host': 'ondeinvestir.lopesfilho.com.br',
        'Pragma': 'no-cache',
        'Referer': 'https://logado.modalmais.com.br/',
        'Sec-Fetch-Mode': 'nested-navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    html = sess.get(HOME_URL, headers=headers).text
    bs = BeautifulSoup(html, 'lxml')
    divs = bs.findAll("div", {"class": "span2"})

    for div in divs:
        empresa = div.attrs.get('data-target').replace('#', '')
        yield empresa


def get_top_pick(empresa):
    sess = requests.Session()

    #URL = 'https://ondeinvestir.lopesfilho.com.br/analises/analise-grafica/modal-data/orientacoes-dia/BMGB4/?callback=jQuery110204247014475648603_1580318896703&_=1580318896705'

    URL = 'https://ondeinvestir.lopesfilho.com.br/analises/analise-grafica/modal-data/orientacoes-dia/%s/?callback=jQuery110204247014475648603_1580318896703&_=1580318896705' % (empresa)


    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=8aq9a87p9rh4apeind522drho1; ARRAffinity=c83c2289f9a097e5bb3a55d79ea33cdbab1c8d9fa07af5e8cc2d1720095ca46b; __utma=262044560.214949217.1575315259.1578334313.1580317431.5; __utmc=262044560; __utmz=262044560.1580317431.5.5.utmcsr=easynvest.com.br|utmccn=(referral)|utmcmd=referral|utmcct=/configuracoes/onde-investir; __utmt=1; __utmb=262044560.23.9.1580318898853',
        'Host': 'ondeinvestir.lopesfilho.com.br',
        'Pragma': 'no-cache',
        'Referer': 'https://ondeinvestir.lopesfilho.com.br/embed/carteiras/carteira-top-picks/',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    # Download do arquivo
    response = sess.get(URL, headers=headers)
    print response.content
    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    for emp in get_home():
        get_top_pick(emp)
