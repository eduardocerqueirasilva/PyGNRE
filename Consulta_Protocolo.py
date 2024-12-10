import requests
from lxml import etree
import base64
import xmlschema



class ConsultaGNRE:
       
    def gerar_corpo_gnre(self, ambiente, numero_recibo, incluir_pdf_guias=None, incluir_arquivo_pagamento=None, incluir_noticias=None):
        gnre = etree.Element('TConsLote_GNRE', xmlns='http://www.gnre.pe.gov.br')
        
        ambiente_elem = etree.SubElement(gnre, 'ambiente')
        ambiente_elem.text = ambiente
        
        numero_recibo_elem = etree.SubElement(gnre, 'numeroRecibo')
        numero_recibo_elem.text = numero_recibo

        if incluir_pdf_guias is not None:
            incluir_pdf_guias_elem = etree.SubElement(gnre, 'incluirPDFGuias')
            incluir_pdf_guias_elem.text = incluir_pdf_guias

        if incluir_arquivo_pagamento is not None:
            incluir_arquivo_pagamento_elem = etree.SubElement(gnre, 'incluirArquivoPagamento')
            incluir_arquivo_pagamento_elem.text = incluir_arquivo_pagamento

        if incluir_noticias is not None:
            incluir_noticias_elem = etree.SubElement(gnre, 'incluirNoticias')
            incluir_noticias_elem.text = incluir_noticias
        
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
        gnre_dados_msg = etree.SubElement(soap_body, 'gnreDadosMsg', xmlns='http://www.gnre.pe.gov.br/webservice/GnreResultadoLote')
        gnre_dados_msg.append(gnre_element)

        return etree.tostring(soap_env, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    
    
    def validar_xml(self, gnre_element):
        schema = xmlschema.XMLSchema('schema/lote_gnre_consulta_v1.00.xsd')  # Adicione o caminho para o seu arquivo XSD
        xml_string = etree.tostring(gnre_element)
        if schema.is_valid(xml_string):
            print("XML válido.")
        else:
            print("XML inválido.", schema.validate(xml_string))

    
    def remove_namespace_xml(self, resposta):
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
    
    

    def base64_para_PDF(self,xml_formatado,incluir_pdf_guias):
        root = etree.fromstring(xml_formatado)
        ns = {'ns': 'http://www.gnre.pe.gov.br'}
        pdf_guias = root.find('.//pdfGuias')
        if incluir_pdf_guias == 'S':
            if (pdf_guias is not None and pdf_guias.text):
                pdf_content = base64.b64decode(pdf_guias.text)
                with open('reports/gnre2.pdf', 'wb') as pdf_file:
                    pdf_file.write(pdf_content)
                print("PDF salvo como gnre.pdf")
            else:
                print("pdfGuias não encontrado na resposta.")
    
    
       
    
    def consultar(self, ambiente, numero_recibo, incluir_pdf_guias=None, incluir_arquivo_pagamento=None, incluir_noticias=None):
        headers = {
            "Content-Type": "application/soap+xml; charset=utf-8",
            "SOAPAction": "http://www.gnre.pe.gov.br/webservice/GnreResultadoLote"
        }        
        url = 'https://www.gnre.pe.gov.br/gnreWS/services/GnreResultadoLote'
        
        gnre_element = self.gerar_corpo_gnre(ambiente, numero_recibo, incluir_pdf_guias, incluir_arquivo_pagamento, incluir_noticias)
        
        # Valida o XML gerado
        self.validar_xml(gnre_element)

        # Cria o envelope SOAP após a validação
        xml_completo = self.gerar_envelope_soap(gnre_element)
        
        session = requests.Session()
        session.verify = True
        session.cert = ('certificados/certificado.pem', 'certificados/chave_certificado.pem')

        try:
            response = session.post(url, data=xml_completo, headers=headers)
            if response.status_code == 200:
                print("Consulta realizada com sucesso!")
                print(response.content)
                xml_formatado = self.remove_namespace_xml(response.content)
                self.base64_para_PDF(xml_formatado,incluir_pdf_guias)
                return xml_formatado
                          
            else:
                print(f"Erro na consulta: {response.status_code}")
                print("Detalhes:", response.content)
                return response.content  # Retorna o conteúdo da resposta em caso de erro
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            return None
