#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : CryptoCurrency Prices
# DESCRIPTION     :
# - 1. Demande à l'utilisateur la crypto dont il veut le prix ou s'il veut
# 	la liste des cryptos disponibles.
# - 2. Cherche la liste des cryptos et les affiches.
# 	Ou cherche le prix via l'API de cryptocompare.com et l'affiche
# - 3. Retour au n°1
# AUTHORS		  : Guillaume HANOTEL
# DATE            : 19/03/2018
# ====================================================


from cryptocompy import coin
from cryptocompy import price
import os
import sys


def get_crypto_full_name(cryptocurrencies):
	"""
	Prend en paramètre la liste complète des cryptomonnaies
	Retourne la liste de seulement les Noms Complets de celles-ci
	"""
	list_names = []
	for key, value in cryptocurrencies.items():
		list_names.append(value.get('FullName'))
	return list_names


def get_crypto_name(cryptocurrencies):
	"""
	Prend en paramètre la liste complète des cryptomonnaies
	Retourne la liste de seulement les Noms de celles-ci
	"""
	list_names = []
	for key, value in cryptocurrencies.items():
		list_names.append(value.get('CoinName'))
	return list_names


def find_key(d, value):
	"""
	Renvoi la liste de toutes les clés parentes de la valeur passé en paramètre dans le
	dic passé en paramètre
	"""
	for k,v in d.items():
		if isinstance(v, dict):
			p = find_key(v, value)
			if p:
				return [k] + p
		elif v == value:
			return [k]


def get_price(cryptocurrency, currency):
	prices_crypto = price.get_current_price(cryptocurrency, [currency], e='all', try_conversion=True, full=False, format='raw')
	return prices_crypto.get(cryptocurrency).get(currency)


def print_price(cryptocurrency, price, currency):
	print('\t1 ' + cryptocurrency + ' = ' + str(price) + symbols.get(currency))
	print('\n')


def print_list(list):
	"""
	Affiche le contenu d'une liste
	"""

	if len(list) % 2 != 0:
		list.append(" ")

	split = int(len(list) / 2)
	l1 = list[0:split]
	l2 = list[split:]

	for key, value in zip(l1, l2):
		print("{0:<40s} {1}".format(key, value))


def clear():
	"""
	Clear l'écran
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


clear()
print("\t*****************************")
print("\t*\tCRYPTOCURRENCY\t    *")
print("\t*****************************")


cryptocurrencies = coin.get_coin_list(coins='all')
cryptocurrencies_names = get_crypto_name(cryptocurrencies)
cryptocurrencies_acronym = cryptocurrencies.keys()
symbols = {'USD': '$', 'EUR': '€'}


while True:

	print("\n - Enter the name or acronym of the cryptocurrency you want")
	print("   (ex : 'BTC' or 'Bitcoin')")
	print(" - Enter 'list' to list cryptocurrency")
	print(" - Enter 'exit' to exit")

	input_cryptocurrency = input("> ")

	if input_cryptocurrency == 'list':
		cryptocurrencies_fullname = list(get_crypto_full_name(cryptocurrencies))
		print_list(cryptocurrencies_fullname)

	elif input_cryptocurrency == 'exit':
		sys.exit(0)

	else:

		# test si l'input (upper) est dans la liste des acronymes
		# ou si l'input est dans la liste des noms des cryptomonnaies
		if input_cryptocurrency.upper() in cryptocurrencies_acronym or input_cryptocurrency in cryptocurrencies_names:
			# si il a entré le nom complet, on le retransforme en acronyme
			if input_cryptocurrency in cryptocurrencies_names:
				input_cryptocurrency = find_key(cryptocurrencies, input_cryptocurrency)[0]

			# récupération des prix
			prix_dollar = get_price(input_cryptocurrency, 'USD')
			print_price(input_cryptocurrency, prix_dollar, 'USD')

		else:
			sys.stderr.write("Error : Undefined CryptoCurrency")
			sys.exit(1)


