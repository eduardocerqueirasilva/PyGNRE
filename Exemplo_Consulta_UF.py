from Consulta_UF import Estrutura_XML_UF_GNRE
from Variaveis import URL_GNRE_CONFIG_UF, PATH
from Comunicacao import Envia_Requisicao
from validadorXML import validar_xml



corpo_xml_uf = Estrutura_XML_UF_GNRE.Corpo_XML_GNRE(
                    ambiente='1', 
                    uf='PR',
                    receita='100099',
                    tiposGnre='S'
                    )
#validar_xml(corpo_xml_uf,f'{PATH}schema/consulta_config_uf_v1.00.xsd')  #VALIDAR O XML DE ENVIO

xml_completo_uf = Estrutura_XML_UF_GNRE.Envelope_SOAP_GNRE(corpo_xml_uf)
#print("XML COMPLETO:" , xml_completo_lote.decode('utf-8'))

# Necessário informar a 'EMPRESA' e o ambiente, pode ser 'producao' ou 'homologacao'
xml_retornado_uf = Envia_Requisicao(
                        empresa='EMPRESA1',
                        ambiente=URL_GNRE_CONFIG_UF["producao"],
                        data=xml_completo_uf,
                        evento_gnre="consultar_uf")

#validar_xml(Estrutura_XML_UF_GNRE.remove_namespace_xml(xml_retornado_uf),f'{PATH}schema/config_uf_v1.00.xsd') #VALIDAR O XML RETORNADO




