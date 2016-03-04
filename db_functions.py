# coding=utf8

#from firebase import firebase
from firebase import Firebase #https://github.com/mikexstudios/python-firebase
import requests


FBURL = 'https://maisbr.firebaseio.com';

def get_lista_codigos_senadores():
	# Retorna lista com códigos de todos os senadores salvos no DB
	# Equivalente ao 'curl' para usar a opção shallow e só pegar as keys dos senadores
	r = requests.get('https://maisbr.firebaseio.com/senadores.json?shallow=True')
	senadores_dict = r.json()

	list = []
	for key, val in senadores_dict.iteritems():
		list.append(key)

	return sorted(list)

def get_nome_from_codigo(codigo):
	# Retorna nome do senador cujo código foi passado no argumento
	f = Firebase(FBURL + '/senadores/' + codigo + '/NomeParlamentar')
	return f.get()

def get_dict_nomes_senadores():
	# Retorna lista com nomes de todos os senadores salvos no DB
	f = Firebase(FBURL + '/senadores')
	dados = f.get()

	dict_nomes = {}
	for key, val in dados.iteritems():
		dict_nomes[key] = val['NomeParlamentar']

	return dict_nomes

def get_votos_senador(codigo):
	#r = requests.get('https://maisbr.firebaseio.com/senadores/' + codigo + '/votos.json')
	#senadores_dict = r.json()

	f = Firebase(FBURL + '/senadores/' + codigo + '/votos')
	senadores_dict = f.get()

	return senadores_dict