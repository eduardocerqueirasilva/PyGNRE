import requests
from lxml import etree
import xmlschema
from validadorXML import validar_xml

class Estrutura_XML_LOTE_GNRE:
    
    def Corpo_XML_GNRE(guias_info):
        # Conteúdo do TLote_GNRE
        TLOTE_GNRE = etree.Element('TLote_GNRE', versao='2.00', xmlns="http://www.gnre.pe.gov.br")
        GUIAS = etree.SubElement(TLOTE_GNRE, 'guias')

        # Adicionando múltiplas guias ao lote
        for guia in guias_info:
            TDADOSGNRE = etree.SubElement(GUIAS, 'TDadosGNRE', versao='2.00')

            etree.SubElement(TDADOSGNRE, 'ufFavorecida').text = guia['ufFavorecida']
            etree.SubElement(TDADOSGNRE, 'tipoGnre').text = guia['tipoGnre']

            # Seção do contribuinte emitente
            CONTRIBUINTE_EMITENTE = etree.SubElement(TDADOSGNRE, 'contribuinteEmitente')
            IDENTIFICACAO = etree.SubElement(CONTRIBUINTE_EMITENTE, 'identificacao')
            etree.SubElement(IDENTIFICACAO, 'IE').text = guia['IE']

            # Seção dos itens GNRE
            ITENS_GNRE = etree.SubElement(TDADOSGNRE, 'itensGNRE')
            ITEM = etree.SubElement(ITENS_GNRE, 'item')

            etree.SubElement(ITEM, 'receita').text = guia['receita']
            DOCUMENTO_ORIGEM = etree.SubElement(ITEM, 'documentoOrigem', tipo=guia['tipoDocumentoOrigem'])
            DOCUMENTO_ORIGEM.text = guia['documentoOrigem']

            etree.SubElement(ITEM, 'dataVencimento').text = guia['dataVencimento']
            VALOR = etree.SubElement(ITEM, 'valor', tipo=guia['tipoValor'])
            VALOR.text = guia['valor']

            # Seção dos campos extras
            CAMPOS_EXTRA = etree.SubElement(ITEM, 'camposExtras')
            CAMPO_EXTRA = etree.SubElement(CAMPOS_EXTRA, 'campoExtra')
            etree.SubElement(CAMPO_EXTRA, 'codigo').text = guia['codigoCampoExtra']
            etree.SubElement(CAMPO_EXTRA, 'valor').text = guia['valorCampoExtra']

            # VALORes totais e data de pagamento
            etree.SubElement(TDADOSGNRE, 'valorGNRE').text = guia['valorGNRE']
            etree.SubElement(TDADOSGNRE, 'dataPagamento').text = guia['dataPagamento']

        return TLOTE_GNRE

    
    
    def Envelope_SOAP_GNRE(corpo_xml):
        # Criando o envelope SOAP com namespaces conforme o WSDL
        ENVELOPE = etree.Element('{http://www.w3.org/2003/05/soap-envelope}Envelope', nsmap={
            'soap12': 'http://www.w3.org/2003/05/soap-envelope',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsd': 'http://www.w3.org/2001/XMLSchema'
        })

        # Cabeçalho SOAP
        HEADER = etree.SubElement(ENVELOPE, '{http://www.w3.org/2003/05/soap-envelope}Header')
        GNRECABECMSG = etree.SubElement(HEADER, 'gnreCabecMsg', xmlns="http://www.gnre.pe.gov.br/wsdl/processar")
        VERSAO_DADOS = etree.SubElement(GNRECABECMSG, 'versaoDados').text = '2.00'

        # Corpo SOAP
        BODY = etree.SubElement(ENVELOPE, '{http://www.w3.org/2003/05/soap-envelope}Body')
        GNRE_DADOS_MSG = etree.SubElement(BODY, 'gnreDadosMsg', xmlns="http://www.gnre.pe.gov.br/webservice/GnreLoteRecepcao")

        if corpo_xml is not None:
            GNRE_DADOS_MSG.append(corpo_xml)
        
        return etree.tostring(ENVELOPE, pretty_print=True, xml_declaration=True, encoding='UTF-8')

         
    
    
    
    
    def extrair_TRetLote_GNRE(resposta):
        root = etree.fromstring(resposta)
        # Registre os namespaces (verifique o seu XML para saber o VALOR correto)
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
    
           
    
    
    def extrair_numero_recibo(tRetLoteGNRE):
        # Registrar namespace para evitar conflitos
        namespaces = {'ns1': 'http://www.gnre.pe.gov.br'}

        # Parsear o XML
        root = etree.fromstring(tRetLoteGNRE)

        # Extrair o VALOR do <ns1:codigo>
        codigo = root.find('.//ns1:codigo', namespaces).text
        print(codigo)

        # Extrair o VALOR do <ns1:numero>
        numero = root.find('.//ns1:numero', namespaces).text
        print(numero)

        if codigo == '100':
            return numero
        else:
            print(f"Falha ao extrair o número do recibo. - Código de situação: {codigo}")
            return None
    


    
                
            
                     
        
        





