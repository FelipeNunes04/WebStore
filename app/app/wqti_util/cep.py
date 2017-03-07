# coding: utf-8
#!/usr/bin/python
# -*- coding: cp1252 -*-

import sys
import urllib
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from xml.dom import pulldom

def buscarcep(cep):
    """
    Localiza o CEP informado no argumento utilizando o serviÃ§o
    disponibilizado pelo site www.buscarcep.com.br. Retorna um
    dicionÃ¡rio contendo as informaÃ§Ãµes obtidas. As chaves retornadas
    sÃ£o: 'cep', 'uf', 'cidade', 'bairro', 'tipo_logradouro', e
    'logradouro'.

    Para avaliar o resultado do retorno, verifique as chaves
    'resultado' e 'resultado_txt'. Para maiores detalhes consulte o
    site do serviÃ§o em www.buscarcep.com.br.
    """
    
    url = urllib.urlopen('http://www.buscarcep.com.br/?cep=' + cep + '&formato=xml&chave=1jyrGffnypeHbXY4YvdX9KhpxzIb4O1')
    #url = urllib.urlopen('http://www.buscarcep.com.br/?cep=' + cep + '&formato=xml&chave=1jyrGffnypeHbXY4YvdX9KhpxzIb4O1')
    #url = urllib.urlopen('http://cep.republicavirtual.com.br/web_cep.php?cep=' + cep + '&formato=xml')

    cepinfo = { 'cep' : '',
                'uf' : '',
                'cidade' : '',
                'bairro' : '',
                'tipo_logradouro' : '',
                'logradouro' : '',
                'resultado' : 0,
                'resultado_txt' : '' }
    
    if url:
        texto = url.read()
        url.close()

        events = pulldom.parseString(texto)
        xpath = ''
        
        for event, node in events:
            if event == pulldom.START_ELEMENT:
                xpath += '/' + node.nodeName

            elif event == pulldom.END_ELEMENT:
                pos = xpath.rfind('/')
                xpath = xpath[0:pos]

            elif event == pulldom.CHARACTERS:
                if xpath == '/webservicecep/retorno/cep':
                    cepinfo['cep'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/uf':
                    cepinfo['uf'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/cidade':
                    cepinfo['cidade'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/bairro':
                    cepinfo['bairro'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/tipo_logradouro':
                    cepinfo['tipo_logradouro'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/logradouro':
                    cepinfo['logradouro'] = node.nodeValue
                    
                elif xpath == '/webservicecep/retorno/resultado':
                    cepinfo['resultado'] = int(node.nodeValue)
                    
                elif xpath == '/webservicecep/retorno/resultado_txt':
                    cepinfo['resultado_txt'] = node.nodeValue
                    
    else:
        # erro na conexÃ£o
        cepinfo['resultado'] = 0
        cepinfo['resultado_txt'] = 'Erro na conexÃ£o'

    return [cepinfo]

def retorna_cep(request, SSL):
    cep = request.GET.get('cep', '')
    objeto = simplejson.dumps(buscarcep(cep))
    return HttpResponse(objeto, mimetype="application/javascript")
    
def busca_cep(request):
    return render_to_response('busca_cep.html')
    
def formata_cep(cep):
    return cep and '%s-%s' % (cep[0:5], cep[5:8]) or ''

def limpa_cep(cep):
    return '%s' % cep.replace('-','').replace('.','')
