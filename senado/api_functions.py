# coding: utf-8
import urllib
import xml.etree.ElementTree  as ET

serviceurl = 'http://legis.senado.gov.br/dadosabertos'
url = '/senador/4981/votacoes'

def tree_from_url(url):
    print 'Getting ET from:', serviceurl + url
    data = urllib.urlopen(serviceurl + url).read()
    tree = ET.fromstring(data)
    try: print tree.find('.//DescricaoDataSet').text
    except: print '(Descrição não encontrada)'
    return tree

def read_url(url):
    print 'Getting data from:', url
    data = urllib.urlopen(url).read()
    return data

def read_serviceurl(url):
    print 'Getting data from:', serviceurl + url
    data = urllib.urlopen(serviceurl + url).read()
    return data

def votacoes_senador(codigo, sigla, numero, ano, tramitando):
    # merging arguments like this doesn't work! Gotta test and only insert if it is not null
    params = {'sigla': sigla, 'numero': numero, 'ano': ano, 'tramitando': tramitando}
    params = {k: v for k, v in params.items() if v}
    print params
    url = serviceurl + '/senador/' + codigo + '/votacoes?' + urllib.urlencode(params)    
    data = urllib.urlopen(url).read()
    tree = ET.fromstring(data)
    print 'Lendo votações de:', serviceurl + url
    try: print tree.find('.//DescricaoDataSet').text
    except: print '(Descrição não encontrada)'
    return tree

def print_xml_element(tree):
	for e in tree.findall('.//'):
		print '<' + e.tag + '>', e.text

def print_xml_element_tags(tree, tag):
	for e in tree.findall('.//' + tag):
		print '<' + e.tag + '>', e.text


# tests
#read_serviceurl(url)
#tree_from_url(url)


