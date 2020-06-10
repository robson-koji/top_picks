
"""
Recupera as indicacoes Top Picks no Onde Investir da Lopes Filho, e envia por e-mail
"""
# -*- coding: utf-8 -*-
import os, sys, time
import requests
import datetime
import json
from bs4 import BeautifulSoup

def get_home():
    """ retorna generator como as empresas recomendadas """

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
    """ Para cada empresa, recupera os parametros de negociacao """

    sess = requests.Session()
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
    content = response.content

    content = content[content.find("{")+1:content.find("}")]
    content = "{" + content + "}"
    content_json = json.loads(content)

    return content_json
    """
    {u'operacao': u'', u'stop-percentual': u'0,00', u'imagem': u'https://ondeinvestireastus.blob.core.windows.net/ag-orientacoes-dia/B3SA3.gif', u'texto': u'Encontrou suporte importantena regi\xe3o dos 42,50, onde come\xe7ou a consolidar e pode voltar a dar sinais de recupera\xe7\xe3o no curto prazo, de olho, inicialmente, no fechamento de gap em 47,82.', u'variacao': u'-2,17', u'tipo': u'SwingTrade', u'volumeEmMilhoes': u'480,71', u'logo-empresa': u'https://ondeinvestireastus.blob.core.windows.net/logotipos/B3.png', u'objetivo2-percentual': u'0,00', u'entrada': u'44,5', u'status': u'Objetivo1 atingido', u'razao-social': u'B3 S.A. - BRASIL, BOLSA, BALC\xc3O', u'stop': u'42,05', u'orientacao': u'Compra', u'objetivo1-percentual': u'0,00', u'volume': u'480.709.259,00', u'objetivo1': u'47,82', u'objetivo2': u'49,5', u'classe-tipo': u'swing-trade', u'class': u'l-up', u'cotacao': u'47,74', u'ifr': u'', u'classe-orientacao': u'compra', u'codigo': u'B3SA3', u'classe-status': u'aguardando'}
    """
    #import pdb; pdb.set_trace()

def get_html(empresa):
    """ Para cada empresa, monta um HTML com os parametros de negociacao """

    html = """<table>
                <tr><td><h2>%s ( %s )</h2></td><td>%s</td></tr>
                <tr><td>%s</td><td>%s</td></tr>
                <tr><td>Entrada </td><td>%s</td></tr>
                <tr><td>Objetivo 1 </td><td>%s</td></tr>
                <tr><td>Objetivo 2 </td><td>%s</td></tr>
                <tr><td>Stop </td><td>%s</td></tr>
                <tr><td colspan=2>%s</td></tr>
            </table><hr>""" % (empresa['codigo'], empresa['orientacao'], empresa['status'],
                            empresa['cotacao'], empresa['variacao'],
                            empresa['entrada'], empresa['objetivo1'],
                            empresa['objetivo2'], empresa['stop'],
                            empresa['texto'])
    return html



def envia_email(html):
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.header import Header

    smtp = smtplib.SMTP()
    smtp.connect('localhost')

    msgRoot = MIMEMultipart("alternative")
    msgRoot['Subject'] = Header("Top Picks", "utf-8")
    msgRoot['From'] = "robson_scripts@contabo.com"
    msgRoot['To'] = "robson.koji@gmail.com"

    html_email = MIMEText(html, 'html', "utf-8")

    msgRoot.attach(html_email)
    smtp.sendmail("root@vmi232710.contaboserver.net", "robson.koji@gmail.com", msgRoot.as_string())


if __name__ == '__main__':
    html = ""

    # Recupera a lista de empresas recomendadas
    for emp in get_home():
        # Para cada empresa, recupera os parametros de negociacao
        content_json = get_top_pick(emp)
        """
        content_json = {u'operacao': u'', u'stop-percentual': u'0,00',
        u'imagem': u'https://ondeinvestireastus.blob.core.windows.net/ag-orientacoes-dia/B3SA3.gif',
        u'texto': u'Encontrou suporte importantena regi\xe3o dos 42,50, onde come\xe7ou a consolidar e pode voltar a dar sinais de recupera\xe7\xe3o no curto prazo, de olho, inicialmente, no fechamento de gap em 47,82.',
        u'variacao': u'-2,17', u'tipo': u'SwingTrade', u'volumeEmMilhoes': u'480,71',
        u'logo-empresa': u'https://ondeinvestireastus.blob.core.windows.net/logotipos/B3.png',
        u'objetivo2-percentual': u'0,00', u'entrada': u'44,5', u'status': u'Objetivo1 atingido',
        u'razao-social': u'B3 S.A. - BRASIL, BOLSA, BALC\xc3O', u'stop': u'42,05', u'orientacao':
        u'Compra', u'objetivo1-percentual': u'0,00', u'volume': u'480.709.259,00',
        u'objetivo1': u'47,82', u'objetivo2': u'49,5', u'classe-tipo': u'swing-trade',
        u'class': u'l-up', u'cotacao': u'47,74', u'ifr': u'', u'classe-orientacao': u'compra',
        u'codigo': u'B3SA3', u'classe-status': u'aguardando'}
        """
        # Para cada empresa, monta um HTML para o email ficar mais amigavel
        html += get_html(content_json)

#    print html
    # Envia email
    envia_email(html)
