import requests
from lxml import etree
import base64

from validadorXML import validar_xml



class Estrutura_XML_CONSULTA_GNRE:
       
    def Corpo_XML_GNRE(ambiente, numero_recibo, incluir_pdf_guias=None, incluir_arquivo_pagamento=None, incluir_noticias=None):
        T_CONS_LOTE_GNRE = etree.Element('TConsLote_GNRE', xmlns='http://www.gnre.pe.gov.br')
        
        AMBIENTE = etree.SubElement(T_CONS_LOTE_GNRE, 'ambiente')
        AMBIENTE.text = ambiente
        
        NUMERO_RECIBO = etree.SubElement(T_CONS_LOTE_GNRE, 'numeroRecibo')
        NUMERO_RECIBO.text = numero_recibo

        if incluir_pdf_guias is not None:
            INCLUIR_PDF_GUIAS = etree.SubElement(T_CONS_LOTE_GNRE, 'incluirPDFGuias')
            INCLUIR_PDF_GUIAS.text = incluir_pdf_guias

        if incluir_arquivo_pagamento is not None:
            INCLUIR_ARQUIVO_PAGAMENTO = etree.SubElement(T_CONS_LOTE_GNRE, 'incluirArquivoPagamento')
            INCLUIR_ARQUIVO_PAGAMENTO.text = incluir_arquivo_pagamento

        if incluir_noticias is not None:
            INCLUIR_NOTICIAS = etree.SubElement(T_CONS_LOTE_GNRE, 'incluirNoticias')
            INCLUIR_NOTICIAS.text = incluir_noticias
        
        return T_CONS_LOTE_GNRE

    
    
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
        GNRE_DADOS_MSG = etree.SubElement(BODY, 'gnreDadosMsg', xmlns='http://www.gnre.pe.gov.br/webservice/GnreResultadoLote')
        
        if corpo_xml is not None:
            GNRE_DADOS_MSG.append(corpo_xml)
        
        return etree.tostring(ENVELOPE, pretty_print=True, xml_declaration=True, encoding='UTF-8')


    
    def remove_namespace_xml(resposta):
        root = etree.fromstring(resposta)
        # Remover todos os atributos do XML de resposta
        for elem in root.iter():
            for attr in list(elem.attrib):
                del elem.attrib[attr]

        # Remover todos os namespaces
        for elem in root.getiterator():
            elem.tag = etree.QName(elem).localname
        etree.cleanup_namespaces(root)

        xml_formatado = etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')
        print("Resposta do servidor sem atributos:", xml_formatado)
                
        return xml_formatado  # Retorna o conteúdo da resposta sem atributos
    
    