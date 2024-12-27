import requests
from lxml import etree

import xmlschema
from validadorXML import validar_xml


import xml.etree.ElementTree as ET



class ConsultaUF:    

    def gerar_corpo_gnre(self, ambiente, uf , receita, tiposGnre):
        gnre = etree.Element('TConsultaConfigUf', xmlns='http://www.gnre.pe.gov.br')
        
        ambiente_elem = etree.SubElement(gnre, 'ambiente')
        ambiente_elem.text = ambiente
        
        uf_elem = etree.SubElement(gnre, 'uf')
        uf_elem.text = uf

        receita_elem = etree.SubElement(gnre, 'receita')
        receita_elem.text = receita

        
        return gnre

    
    def gerar_envelope_soap(self, gnre_element):
        soap_env = etree.Element('{http://www.w3.org/2003/05/soap-envelope}Envelope', nsmap={
            'soapenv': 'http://www.w3.org/2003/05/soap-envelope',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema'
        })

        soap_header = etree.SubElement(soap_env, '{http://www.w3.org/2003/05/soap-envelope}Header')
        gnre_cabecalho_soap = etree.SubElement(soap_header, 'gnreCabecMsg', xmlns='http://www.gnre.pe.gov.br/wsdl/consultar')
        versao_dados = etree.SubElement(gnre_cabecalho_soap, 'versaoDados')
        versao_dados.text = '2.00'

        soap_body = etree.SubElement(soap_env, '{http://www.w3.org/2003/05/soap-envelope}Body')
        gnre_dados_msg = etree.SubElement(soap_body, 'gnreDadosMsg', xmlns='http://www.gnre.pe.gov.br/webservice/GnreConfigUF')
        gnre_dados_msg.append(gnre_element)

        return etree.tostring(soap_env, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    

    
    
    def consultar(self, ambiente, uf , receita, tiposGnre):
        headers = {'Content-Type': 'application/soap+xml;charset=utf-8',
                    'SOAPAction': 'https://www.gnre.pe.gov.br/gnreWS/services/GnreConfigUF'}
        url = 'https://www.gnre.pe.gov.br/gnreWS/services/GnreConfigUF'
        gnre_element = self.gerar_corpo_gnre(ambiente, uf , receita, tiposGnre)
        
        # Valida o XML gerado
        validar_xml(gnre_element,'schema/consulta_config_uf_v1.00.xsd')

        # Cria o envelope SOAP após a validação
        data = self.gerar_envelope_soap(gnre_element)
        
        session = requests.Session()
        session.verify = True
        session.cert = ('certificados/certificado.pem', 'certificados/chave_certificado.pem')

        try:
            response = session.post(url, data=data, headers=headers)
            if response.status_code == 200:
                print("Consulta realizada com sucesso!")
                
                root = etree.fromstring(response.content)

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
                    response_content = etree.tostring(tconfiguf, encoding='unicode')
                else:
                    print("Elemento TConfigUf não encontrado.")

                print(response_content)
                
    
                return response_content  # Retorna o conteúdo da resposta sem atributos
            else:
                print(f"Erro na consulta: {response.status_code}")
                print("Detalhes:", response.content)
                return response.content  # Retorna o conteúdo da resposta em caso de erro
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            return None


    



# Exemplo de uso 

retorno_consulta = ConsultaUF().consultar('1', 'PR','100099','S') 

ConsultaUF().validar_xml(retorno_consulta,'schema/config_uf_v1.00.xsd')



