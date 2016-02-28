# coding=utf8

import api_functions as af
import db_functions  as db
import urllib
import xml.etree.ElementTree  as ET
import xmltodict, json
#from firebase import firebase
from firebase import Firebase #https://github.com/mikexstudios/python-firebase
import time

FBURL = 'https://maisbr.firebaseio.com';

#af.get_materias_from_list(af.pesquisa_materia({'palavraChave':'abacaxi'}))

#firebase = firebase.FirebaseApplication('https://maisbr.firebaseio.com', None)
#f = Firebase('https://maisbr.firebaseio.com/')

def get_senadores_metadata_atual():
	# Gets attributes from parlamentares and saves into Firebase 
	# --> still needs to put right below 'senadores URL', now it's using FB id there...

	url = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
	uh = urllib.urlopen(url)
	data = uh.read()
	tree = ET.fromstring(data)
	senadores_tree = tree.findall('.//IdentificacaoParlamentar')
	
	senadores_dict = {}
	for sen in senadores_tree:
		
		codigo = sen.find('CodigoParlamentar').text
		# creates object with id 'codigo' and all data nested into that
		senadores_dict[codigo] = {}
		senadores_dict[codigo]['NomeParlamentar'] 			= sen.find('NomeParlamentar').text
		senadores_dict[codigo]['SexoParlamentar'] 			= sen.find('SexoParlamentar').text
		senadores_dict[codigo]['FormaTratamento'] 			= sen.find('FormaTratamento').text
		senadores_dict[codigo]['UrlPaginaParlamentar']		= sen.find('UrlPaginaParlamentar').text
		senadores_dict[codigo]['UrlFotoParlamentar']		= sen.find('UrlFotoParlamentar').text
		senadores_dict[codigo]['EmailParlamentar'] 			= sen.find('EmailParlamentar').text
		senadores_dict[codigo]['SiglaPartidoParlamentar'] 	= sen.find('SiglaPartidoParlamentar').text
		senadores_dict[codigo]['UfParlamentar'] 			= sen.find('UfParlamentar').text

	#firebase.post('/senadores', senadores_dict) # Substituir posteriormente por método genérico para salvar os dados
	f = Firebase(FBURL + '/senadores')
	f.put(senadores_dict)


def get_votacoes_senador(codigo):
	# Salva votações do senador no banco de dados
	# !!! Se a matéria foi votada mais de uma vez (em diferentes tramitações), somente um voto é guardado
	# |_ isso depende de qual for colocado por último no XML (elaborar rotina para ordenar por data!)
	tree = af.votacoes_senador(codigo, {'ano':'2015', 'sigla':'PEC'})
	votacoes_tree = tree.findall('.//Votacao')

	# Inicialização com possíveis valores de votação
	votos_dict = {
	'Sim' 	: {},
	'Nao' 	: {},
	'PNRV' 	: {},
	'MIS' 	: {},
	'LS' 	: {},
	'Outro'	: {}
	}	

	for vot in votacoes_tree:
		
		voto = vot.find('.//DescricaoVoto').text

		# Testes "frágeis" para adaptar nome das keys, os tipos são somente esses. Primeiro caracter somente para fugir de probs. de codificiação (unicode). Arrumar futuramente!
		if 	 voto[:1] == 'S'	: voto = 'Sim'
		elif voto[:1] == 'N'	: voto = 'Nao'
		elif voto[:1] == 'M'	: voto = 'MIS'
		elif voto[:1] == 'P'	: voto = 'PNRV'
		elif voto[:1] == 'L '	: voto = 'LS'
		else: 					  voto = 'Outro'

		cod_materia = vot.find('.//CodigoMateria').text

		print cod_materia, voto

		votos_dict[voto][cod_materia] = {}
		votos_dict[voto][cod_materia]['DescricaoVoto'] 				= vot.find('.//DescricaoVoto').text
		votos_dict[voto][cod_materia]['DescricaoVotacao'] 		= vot.find('.//DescricaoVotacao').text
		votos_dict[voto][cod_materia]['DescricaoResultado'] 	= vot.find('.//DescricaoResultado').text
		votos_dict[voto][cod_materia]['AnoMateria'] 			= vot.find('.//AnoMateria').text
		votos_dict[voto][cod_materia]['SiglaSubtipoMateria'] 	= vot.find('.//SiglaSubtipoMateria').text
	
	# Salva no Firebase
	url = '/senadores/' + codigo + '/votos/'
	f = Firebase(FBURL + url)
	f.put(votos_dict)

	#firebase.post('/senadores', senadores_dict)

def get_materias_metadata_atual():
	# Definir quão atuais são as matérias (fetch by date, maybe? By number intrinsically is by date?)
	pass

def test_firebase():
	test_data = {'name':'cleibzon', 'materias':['a','b','c']}
	firebase.post('/test', test_data)

def get_votos_senadores():
	# Assume que senadores já estão salvos no Firebase
	sen_list = db.get_senadores_list()

	for codigo_senador in sen_list:
		print 'Preenchendo senador:', codigo_senador
		get_votacoes_senador(codigo_senador)

get_senadores_metadata_atual()
time.sleep(5) # Waits for data to be loaded
get_votos_senadores()



