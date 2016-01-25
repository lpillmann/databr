# coding: utf-8
import urllib
import xml.etree.ElementTree as ET

url = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
uh = urllib.urlopen(url)
data = uh.read()
tree = ET.fromstring(data)
senadores = tree.findall('.//Parlamentar')
codigos = tree.findall('.//Parlamentar/IdentificacaoParlamentar/CodigoParlamentar')

url_sen = 'http://legis.senado.gov.br/dadosabertos/senador/'

dados=[]
for c in codigos:
    url = url_sen + str(c.text)
    data = urllib.urlopen(url).read()
    tree = ET.fromstring(data)
    nome = tree.find('.//NomeCompletoParlamentar')
    materias = tree.findall('.//Materia')
    print nome.text, len(materias)
    dados.append([c.text, nome.text, len(materias)])
    
nomes = []
materias = []
keys = []

for i in dados:
    print i[0]
    keys.append(i[0])
    print i[1]
    print i[2]
    print '---'
    nomes.append(i[1])
    materias.append(i[2])
    
nomes_materias = dict(zip(nomes, materias))

import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3

conn = sqlite3.connect('parlamentares_materias.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Materias''')

cur.execute('''
CREATE TABLE Materias (nome TEXT, materias INTEGER)''')

for i in range(len(nomes)):    
    cur.execute('''INSERT INTO Materias (nome, materias) 
    VALUES (?, ?)''', (nomes[i], materias[i]) )
    
conn.commit()

sqlcmd = 'SELECT nome, materias FROM Materias ORDER BY materias DESC'
cur.execute(sqlcmd)
res = cur.fetchall()

data = [
go.Bar(
	x=[i[0] for i in res],
	y=[i[1] for i in res]
)
]

plot_url = py.plot(data)
