from Consulta_UF import Estrutura_XML_UF_GNRE
from Variaveis import EVENTO_GNRE, URL_GNRE_CONFIG_UF
from Comunicacao import Envia_Requisicao
from validadorXML import validar_xml



corpo_xml_uf = Estrutura_XML_UF_GNRE.Corpo_XML_GNRE('1', 'PR','100099','S')
#validar_xml(corpo_xml_lote,'schema/consulta_config_uf_v1.00.xsd')  #VALIDAR O XML DE ENVIO

xml_completo_uf = Estrutura_XML_UF_GNRE.Envelope_SOAP_GNRE(corpo_xml_uf)
#print("XML COMPLETO:" , xml_completo_lote.decode('utf-8'))

# Necessário informar a 'EMPRESA' e o ambiente, pode ser 'producao' ou 'homologacao'
xml_retornado_uf = Envia_Requisicao('EMPRESA1',URL_GNRE_CONFIG_UF["producao"],xml_completo_uf,EVENTO_GNRE["consultar_uf"])

validar_xml(Estrutura_XML_UF_GNRE.remove_namespace_xml(xml_retornado_uf),'schema/config_uf_v1.00.xsd') #VALIDAR O XML RETORNADO




