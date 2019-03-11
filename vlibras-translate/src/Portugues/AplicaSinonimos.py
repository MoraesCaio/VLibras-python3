#!/usr/bin/python
# -*- coding: utf-8 -*-

# Autor: Erickson Silva
# Email: <erickson.silva@lavid.ufpb.br> <ericksonsilva@live.com>

# LAViD - Laboratório de Aplicações de Vídeo Digital

import os
import re
import csv
import sys
from nltk.tree import Tree
from LerDicionarios import *
from os.path import expanduser
from os import environ, path


class AplicaSinonimos(object):
    '''Aplica sinonimos após aplicação de regras morfológicas/sintática
    '''

    def __init__(self):
        self.dicionarios = LerDicionarios()
        self.ordinais = {u'8\xaa': u'oitava', u'3\xba': u'terceiro', u'9\xaa': u'nona', u'5\xba': u'quinto', u'6\xaa': u'sexta',
                         u'1\xba': u'primeiro', u'7\xaa': u's\xe9tima', u'2\xba': u'segundo', u'8\xba': u'oitavo', u'3\xaa': u'terceira',
                                                        u'9\xba': u'nono', u'5\xaa': u'quinta', u'6\xba': u'sexto', u'1\xaa': u'primeira', u'7\xba': u's\xe9timo', u'2\xaa': u'segunda'}

    # Itera sobre os tokens obtendo os sinonimos
    def aplicar_sinonimos(self, lista_anotada):
        '''Percorre a lista fazendo a substituição pelos sinonimos.
        '''
        lista_corrigida = []
        print('AplicaSinonimos aplicar_sinonimos l34:\n', lista_anotada)
        for tupla in lista_anotada:
            sinonimo = tupla[0].upper()
            #sinonimo = self.verificar_sinonimo(tupla[0].upper())
            if tupla[1] == "NUM" or tupla[1] == "NUM-R":
                if self.verificar_ordinal(sinonimo):
                    ordinal = self.get_ordinal_extenso(sinonimo)
                    lista_corrigida.append(ordinal)
                    continue
                else:
                    cardinal = self.converter_ordinal_para_cardinal(sinonimo)
                    lista_corrigida.append(cardinal)
                    print('AplicaSinonimos aplicar_sinonimos l46:\n', cardinal)
                    continue
            lista_corrigida.append(sinonimo)
        print(lista_corrigida)
        return self.verificar_palavra_composta(lista_corrigida)

    # Verifica se há sinonimo do token
    def verificar_sinonimo(self, token):
        '''Verifica se há sinonimo do token.
        '''
        if self.dicionarios.has_sinonimo(token):
            return self.dicionarios.get_sinonimo(token)
        return token

    def verificar_palavra_composta(self, lista):
        palavras_compostas = self.carregar_palavras_compostas()
        try:
            sentenca_corrigida = "_".join(lista).upper()
        except:
            sentenca_corrigida = "_".join([str(x[0]) for x in lista]).upper()
        for p in palavras_compostas:
            for m in re.finditer(p, sentenca_corrigida):
                first = "_" if m.start(
                ) == 0 else sentenca_corrigida[m.start() - 1]
                last = "_" if m.end() == len(
                    sentenca_corrigida) else sentenca_corrigida[m.end() - 1]
                if first == "_" and last == "_":
                    sentenca_corrigida = sentenca_corrigida.replace(
                        p, p.replace("_", "#*#"))
        return sentenca_corrigida.replace("_", " ").replace("#*#", "_")

    def carregar_palavras_compostas(self):
        path = self.localizar_arquivo_palavras_compostas()
        return set(open(path).read().decode('utf-8').split())

    def localizar_arquivo_palavras_compostas(self):
        if "TRANSLATE_DATA" in environ:
            return path.join(environ.get("TRANSLATE_DATA"), "palavras_compostas.csv")
        return expanduser("~") + '/vlibras-translate/data/palavras_compostas.csv'

    def get_ordinal_extenso(self, token):
        return self.ordinais[token]

    def verificar_ordinal(self, token):
        return self.ordinais.has_key(token)

    def converter_ordinal_para_cardinal(self, token):
        return token.replace("ª".decode('utf-8'), "").replace("º".decode('utf-8'), "")
