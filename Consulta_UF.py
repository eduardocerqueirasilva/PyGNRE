import requests
from lxml import etree

import xmlschema
from validadorXML import validar_xml


import xml.etree.ElementTree as ET



class Estrutura_XML_UF_GNRE:    

    def Corpo_XML_GNRE(ambiente, uf , receita, tiposGnre):
        T_CONSULTA_CONFIG_UF = etree.Element('TConsultaConfigUf', xmlns='http://www.gnre.pe.gov.br')
        
        AMBIENTE = etree.SubElement(T_CONSULTA_CONFIG_UF, 'ambiente')
        AMBIENTE.text = ambiente
        
        UF = etree.SubElement(T_CONSULTA_CONFIG_UF, 'uf')
        UF.text = uf

        RECEITA = etree.SubElement(T_CONSULTA_CONFIG_UF, 'receita')
        RECEITA.text = receita
       
        return T_CONSULTA_CONFIG_UF

    
    def Envelope_SOAP_GNRE(corpo_xml):
        ENVELOPE = etree.Element('{http://www.w3.org/2003/05/soap-envelope}Envelope', nsmap={
            'soapenv': 'http://www.w3.org/2003/05/soap-envelope',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema'
        })

        HEADER = etree.SubElement(ENVELOPE, '{http://www.w3.org/2003/05/soap-envelope}Header')
        GNRE_CABEC_MSG = etree.SubElement(HEADER, 'gnreCabecMsg', xmlns='http://www.gnre.pe.gov.br/wsdl/consultar')
        VERSAO_DADOS = etree.SubElement(GNRE_CABEC_MSG, 'versaoDados')
        VERSAO_DADOS.text = '2.00'

        BODY = etree.SubElement(ENVELOPE, '{http://www.w3.org/2003/05/soap-envelope}Body')
        GNRE_DADOS_MSG = etree.SubElement(BODY, 'gnreDadosMsg', xmlns='http://www.gnre.pe.gov.br/webservice/GnreConfigUF')

        if corpo_xml is not None:
            GNRE_DADOS_MSG.append(corpo_xml)
        
        return etree.tostring(ENVELOPE, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    

    def remove_namespace_xml(resposta):

        root = etree.fromstring(resposta)

        # Registre os namespaces (verifique o seu XML para saber o valor correto)
        # Registre os namespaces usados no XML
        namespaces = {
            'soapenv': "http://www.w3.org/2003/05/soap-envelope",
            'gnre': "http://www.gnre.pe.gov.br/webservice/GnreConfigUF",
            'ns1': "http://www.gnre.pe.gov.br"
        }

        # Busca pelo elemento TConfigUf usando o namespace registrado
        tconfiguf = root.find('.//ns1:TConfigUf', namespaces)
        if tconfiguf is not None:
            # Retorna todos os filhos do TConfigUf como XML
            tconfiguf = etree.tostring(tconfiguf, encoding='unicode')
        else:
            print("Elemento TConfigUf não encontrado.")

        return tconfiguf

    



    







