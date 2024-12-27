import requests
from lxml import etree
import xmlschema

class GeraLoteGNRE:
    def __init__(self, ambiente):
               
        # URLs para homologação e produção
        self.url_homologacao = "https://www.testegnre.pe.gov.br/gnreWS/services/GnreLoteRecepcao"
        self.url_producao = "https://www.gnre.pe.gov.br/gnreWS/services/GnreLoteRecepcao"

        # Escolhendo a URL com base no ambiente
        self.url = self.url_homologacao if ambiente == 'homologacao' else self.url_producao

    
    def gera_lote_guias(self, guias_info):
        # Conteúdo do TLote_GNRE
        lote_gnre = etree.Element('TLote_GNRE', versao='2.00', xmlns="http://www.gnre.pe.gov.br")
        guias = etree.SubElement(lote_gnre, 'guias')

        # Adicionando múltiplas guias ao lote
        for guia in guias_info:
            dados_gnre = etree.SubElement(guias, 'TDadosGNRE', versao='2.00')

            etree.SubElement(dados_gnre, 'ufFavorecida').text = guia['ufFavorecida']
            etree.SubElement(dados_gnre, 'tipoGnre').text = guia['tipoGnre']

            # Seção do contribuinte emitente
            contribuinte_emitente = etree.SubElement(dados_gnre, 'contribuinteEmitente')
            identificacao = etree.SubElement(contribuinte_emitente, 'identificacao')
            etree.SubElement(identificacao, 'IE').text = guia['IE']

            # Seção dos itens GNRE
            itens_gnre = etree.SubElement(dados_gnre, 'itensGNRE')
            item = etree.SubElement(itens_gnre, 'item')

            etree.SubElement(item, 'receita').text = guia['receita']
            documento_origem = etree.SubElement(item, 'documentoOrigem', tipo=guia['tipoDocumentoOrigem'])
            documento_origem.text = guia['documentoOrigem']

            etree.SubElement(item, 'dataVencimento').text = guia['dataVencimento']
            valor = etree.SubElement(item, 'valor', tipo=guia['tipoValor'])
            valor.text = guia['valor']

            # Seção dos campos extras
            campos_extras = etree.SubElement(item, 'camposExtras')
            campo_extra = etree.SubElement(campos_extras, 'campoExtra')
            etree.SubElement(campo_extra, 'codigo').text = guia['codigoCampoExtra']
            etree.SubElement(campo_extra, 'valor').text = guia['valorCampoExtra']

            # Valores totais e data de pagamento
            etree.SubElement(dados_gnre, 'valorGNRE').text = guia['valorGNRE']
            etree.SubElement(dados_gnre, 'dataPagamento').text = guia['dataPagamento']

        return lote_gnre

    
    
    def xml_envio_completo(self,lote_gnre):
        # Criando o envelope SOAP com namespaces conforme o WSDL
        env = etree.Element('{http://www.w3.org/2003/05/soap-envelope}Envelope', nsmap={
            'soap12': 'http://www.w3.org/2003/05/soap-envelope',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema'
        })

        # Cabeçalho SOAP
        header = etree.SubElement(env, '{http://www.w3.org/2003/05/soap-envelope}Header')
        gnre_cabec_msg = etree.SubElement(header, 'gnreCabecMsg', xmlns="http://www.gnre.pe.gov.br/wsdl/processar")
        versao_dados = etree.SubElement(gnre_cabec_msg, 'versaoDados').text = '2.00'

        # Corpo SOAP
        body = etree.SubElement(env, '{http://www.w3.org/2003/05/soap-envelope}Body')
        gnre_dados_msg = etree.SubElement(body, 'gnreDadosMsg', xmlns="http://www.gnre.pe.gov.br/webservice/GnreLoteRecepcao")
        gnre_dados_msg.append(lote_gnre)
        
        return etree.tostring(env, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    
    def validar_xml_envio_lote(self,xml_envio_lote):
        print('\nINICIANDO VALIDAÇÂO DO LOTE DE ENVIO\n')
        xsd_path_envio = xmlschema.XMLSchema('schema/lote_gnre_v2.00.xsd')       
        xml_string = etree.tostring(xml_envio_lote)
        
        if xsd_path_envio.is_valid(xml_string):
            print("XML de Envio do Lote validado com sucesso")
        else:
            print("Erro no XML de Envio do Lote")
            print(xsd_path_envio.validate(xml_string))

       
    
    
    def extrair_TRetLote_GNRE(self, resposta):
        root = etree.fromstring(resposta)
        # Registre os namespaces (verifique o seu XML para saber o valor correto)
        namespaces = {
            'soapenv': "http://www.w3.org/2003/05/soap-envelope",
            'gnre': "http://www.gnre.pe.gov.br/webservice/GnreConfigUF",
            'ns1': "http://www.gnre.pe.gov.br"
        }

        # Busca pelo elemento TRetLote_GNRE usando o namespace registrado
        tRetLoteGNRE = root.find('.//ns1:TRetLote_GNRE', namespaces)
        if tRetLoteGNRE is not None:
            # Retorna todos os filhos do TRetLote_GNRE como XML
            tRetLoteGNRE = etree.tostring(tRetLoteGNRE, encoding='unicode')
        else:
            print("Elemento TRetLote_GNRE não encontrado.")
        print("Somente TRetLote_GNRE\n",tRetLoteGNRE)
                    
        return tRetLoteGNRE
    
    
    
    def validar_xml_retorno_lote(self,xml_retorno_lote):
        print('\nINICIANDO VALIDAÇÂO DO LOTE DE RETORNO\n')
        xsd_path_envio = xmlschema.XMLSchema('schema/lote_gnre_recibo_v1.00.xsd')       
        if xsd_path_envio.is_valid(xml_retorno_lote):
            print("XML de Retorno do Lote validado com sucesso")
        else:
            print("Erro no XML de Retorno do Lote")
            print(xsd_path_envio.validate(xml_retorno_lote))
        
    
    
    def extrair_numero_recibo(self,tRetLoteGNRE):
        # Registrar namespace para evitar conflitos
        namespaces = {'ns1': 'http://www.gnre.pe.gov.br'}

        # Parsear o XML
        root = etree.fromstring(tRetLoteGNRE)

        # Extrair o valor do <ns1:codigo>
        codigo = root.find('.//ns1:codigo', namespaces).text
        print(codigo)

        # Extrair o valor do <ns1:numero>
        numero = root.find('.//ns1:numero', namespaces).text
        print(numero)

        if codigo == '100':
            return numero
        else:
            print(f"Falha ao extrair o número do recibo. - Código de situação: {codigo}")
            return None
    


    def geraGuias(self, lote_guias):
        # Gerando e exibindo o XML com múltiplas guias
        
        #Validando o xml criado com o XSD        
        self.validar_xml_envio_lote(lote_guias)
        # Montando o XML completo para enviar
        xml_lote_gnre = self.xml_envio_completo(lote_guias)
        
        print("XML LOTE GNRE " + xml_lote_gnre.decode('utf-8'))
        

        # Configuração e envio da requisição
        session = requests.Session()
        session.verify = True
        session.cert = ('certificados/certificado.pem', 'certificados/chave_certificado.pem')
        headers = {
            "Content-Type": "application/soap+xml; charset=utf-8",
            "SOAPAction": "http://www.gnre.pe.gov.br/webservice/GnreLoteRecepcao/processar"
        }

        # Envio da requisição
        try:
            response = session.post(self.url, data=xml_lote_gnre, headers=headers)
            if response.status_code == 200:
                print("Lote enviado com sucesso!\n",response.content)
                
                retorno_lote = self.extrair_TRetLote_GNRE(response.content)                
                self.validar_xml_retorno_lote(retorno_lote)
                numero_recibo = self.extrair_numero_recibo(retorno_lote)
                return numero_recibo
                
            else:
                return f"Erro no envio do lote: {response.status_code} - {response.content}"
        
             
        
        
        except requests.exceptions.RequestException as e:
            return f"Erro de conexão: {e}"





