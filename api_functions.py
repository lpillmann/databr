# coding: utf-8
import urllib
import xml.etree.ElementTree  as ET
import xmltodict, json

serviceurl = 'http://legis.senado.gov.br/dadosabertos'
url = '/senador/4981/votacoes'

def data_from_url(url):
    print 'Getting data from:', url
    data = urllib.urlopen(url).read()
    return data

def data_from_serviceurl(url):
    print 'Getting data from:', serviceurl + url
    data = urllib.urlopen(serviceurl + url).read()
    return data

def tree_from_url(url):
    data = data_from_url(url)
    tree = ET.fromstring(data)
    try: print 'Descrição dos dados:', tree.find('.//DescricaoDataSet').text
    except: print '(Descrição não encontrada)'
    return tree

def tree_from_serviceurl(url):
    data = data_from_serviceurl(url)
    tree = ET.fromstring(data)
    try: print 'Descrição dos dados:', tree.find('.//DescricaoDataSet').text
    except: print '(Descrição não encontrada)'
    return tree

def tree_from_serviceurl_params(url, params):
    # Returns XML tree according to URL and parameters
    # Example tree_from_url_params('/materia/pesquisa/lista?', {'ano' : '2014'})
    # @params: object with desired parameters
    url = serviceurl + url + urllib.urlencode(params)    
    tree = tree_from_url(url)
    return tree

def print_xml_element(tree):
    for e in tree.findall('.//'):
        print '<' + e.tag + '>', e.text

def print_xml_element_tags(tree, tag):
    # Prints tags and content for a desired tree. Returns list of values
    data = []
    for e in tree.findall('.//' + tag):
        print '<' + e.tag + '>', e.text
        data.append(e.text);
    return  data

#def get_tag_content(tree):


def votacoes_senador(codigo, sigla, numero, ano, tramitando):
    # Retorna tree XML com todas as votações do mandato do senador, sujeito aos parâmetros
    # --> Processar dados para extrair somente infos relevantes
    # --> Avaliar usar objeto de parâmetros como argumento em vez de tudo separado
    # @codigo:      código do senador
    # @sigla:       (opcional) sigla da matéria - retorna apenas as matérias da sigla informada.
    # @numero:      (opcional) número da matéria - retorna apenas as matérias do número informado.
    # @ano:         (opcional) ano da matéria - retorna apenas as matérias do ano informado
    # @tramitacao:  (opcional) (S ou N) - retorna apenas as matérias que estão tramitando (S) ou apenas as que não estão (N). Se não for informado, retorna ambas.

    params = {'sigla': sigla, 'numero': numero, 'ano': ano, 'tramitando': tramitando}
    params = {k: v for k, v in params.items() if v} # eliminates empty parameters
    print 'Votações do senador:', codigo, params
    url = '/senador/' + codigo + '/votacoes?'
    tree = tree_from_serviceurl_params(url, params)
    # Print specific characteristic for the dataset
    try: print 'Nome:', tree.find('.//NomeParlamentar').text
    except: print '(Nome não encontrado)'
    return tree

def pesquisa_materia(params):
    # Searches for 'materias' that match given parameters
    # Docs: <http://legis.senado.gov.br/dadosabertos/docs/path__materia_pesquisa_lista.html>
    aux = tree_from_serviceurl_params('/materia/pesquisa/lista?', params)
    return print_xml_element_tags(aux,'CodigoMateria')

def get_materia(codigo):
    url = '/materia/' + codigo
    aux = tree_from_serviceurl(url)
    print_xml_element_tags(aux,'EmentaMateria')
    return aux

def get_materias_from_list(lista):
    # @lista: python list with strings of codigos
    for item in lista:
        get_materia(item)
        print '-----------------------------------------------------------'



# Tests: paste into IPython
#votacoes_senador('4981', 'PLS','','','')
#tree_from_serviceurl_params('/materia/pesquisa/lista?', {'ano' : '2014'})
#pesquisa_materia({'palavraChave':'aborto'})
#get_materias_from_list(pesquisa_materia({'palavraChave':'abacaxi'}))



