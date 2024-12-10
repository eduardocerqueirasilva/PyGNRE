from Envio_Lote import GeraLoteGNRE
from Consulta_Protocolo import ConsultaGNRE
from guias import lista_de_guias
from report import xml_to_pdf

loteGNRE = GeraLoteGNRE(ambiente='producao')
recibo = loteGNRE.geraGuias(lista_de_guias)

if recibo:
    # Exemplo de uso
    xml = ConsultaGNRE().consultar(ambiente='1', numero_recibo=recibo, incluir_pdf_guias='S', incluir_arquivo_pagamento='N', incluir_noticias='N')
    xml_to_pdf(xml)