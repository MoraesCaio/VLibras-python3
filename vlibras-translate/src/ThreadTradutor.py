#!/usr/bin/python
# -*- coding: utf-8 -*-

# Autor: Erickson Silva
# Email: <erickson.silva@lavid.ufpb.br> <ericksonsilva@live.com>

# LAViD - Laboratório de Aplicações de Vídeo Digital

from TraduzSentencas import *
from threading import Thread
import re


class ThreadTradutor(Thread):
    '''Thread que inicia uma tradução'''

    def __init__(self, sentenca, taxa, lang="pt_br"):
        ''' Recebe o texto a ser traduzido e o atribui a uma variável.
        Além disso, instancia variável que será armazenada a glosa e a classe responsável pelo processo de tradução.
        '''
        Thread.__init__(self)
        self.sentenca = sentenca
        self.glosa = ""
        self.tradutor = TraduzSentencas(lang)
        self.taxa_qualidade = taxa

    def run(self):
        ''' Metódo executado ao 'startar' a Thread. É responsável por iniciar a tradução passando o texto como parâmetro.
        '''
        # sentencas, fins_de_sentenca = self.separar_sentenças(self.sentenca)

        # for sentenca in sentencas:

        self.glosa += self.tradutor.iniciar_traducao(self.sentenca, self.taxa_qualidade)

        # if fins_de_sentenca:
        #     self.glosa += fins_de_sentenca.pop(0)

        print('GLOSA:', self.glosa)

    def obter_glosa(self):
        ''' Obtém a glosa após o processo de tradução.
        '''
        return self.glosa

    def substituir_SPT(self):
        pass

    def separar_sentenças(self, sentenca):
        lista_sentencas = [token for token in re.split('[?=\?\!\.]+', sentenca) if token]
        fins_de_sentenca = [token for token in re.findall('[?=\?\!\.]+', sentenca) if token]
        return lista_sentencas, fins_de_sentenca
