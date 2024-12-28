from Envio_Lote_GNRE import Estrutura_XML_LOTE_GNRE
from Consulta_Protocolo import Estrutura_XML_CONSULTA_GNRE
from guias import lista_de_guias
from report import xml_to_pdf
from Variaveis import URL_GNRE_LOTE, URL_GNRE_CONSULTA
from Comunicacao import Envia_Requisicao
from validadorXML import validar_xml



corpo_xml_lote = Estrutura_XML_LOTE_GNRE.Corpo_XML_GNRE(lista_de_guias)
#validar_xml(corpo_xml,'schema/lote_gnre_v2.00.xsd')  #VALIDAR O XML DE ENVIO

xml_completo_lote = Estrutura_XML_LOTE_GNRE.Envelope_SOAP_GNRE(corpo_xml_lote)
#print("XML COMPLETO:" , xml_completo.decode('utf-8'))

# Necessário informar a 'EMPRESA' e o ambiente, pode ser 'producao' ou 'homologacao'
xml_retornado_lote = Envia_Requisicao(
                        empresa='EMPRESA1',
                        ambiente=URL_GNRE_LOTE["producao"],
                        data=xml_completo_lote,
                        evento_gnre="processar"
                        )

#validar_xml(Estrutura_XML_LOTE_GNRE.extrair_TRetLote_GNRE(xml_retornado),'schema/lote_gnre_recibo_v1.00.xsd') #VALIDAR O XML RETORNADO

recibo = Estrutura_XML_LOTE_GNRE.extrair_numero_recibo(xml_retornado_lote)


if recibo:
    # Exemplo de uso
    corpo_xml_consulta = Estrutura_XML_CONSULTA_GNRE.Corpo_XML_GNRE(
                            ambiente='1', 
                            numero_recibo=recibo, 
                            incluir_pdf_guias='S', 
                            incluir_arquivo_pagamento='N', 
                            incluir_noticias='N'
                            )    
    
    validar_xml(corpo_xml_consulta,'schema/lote_gnre_consulta_v1.00.xsd') # Valida o XML gerado
    
    
    xml_completo_consulta = Estrutura_XML_CONSULTA_GNRE.Envelope_SOAP_GNRE(corpo_xml_consulta)
    
    # Necessário informar a 'EMPRESA' e o ambiente, pode ser 'producao' ou 'homologacao'
    xml_retornado_consulta = Envia_Requisicao(
                                empresa='EMPRESA1',
                                ambiente=URL_GNRE_CONSULTA["producao"],
                                data=xml_completo_consulta,
                                evento_gnre="consultar"
                                )

    xml_formatado = Estrutura_XML_CONSULTA_GNRE.remove_namespace_xml(xml_retornado_consulta)
    
    xml_to_pdf(xml_formatado,to_base64=True, nome="GNRE")