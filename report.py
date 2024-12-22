# -*- coding: utf-8 -*-
import os
import tempfile
from pyreportjasper import PyReportJasper
from lxml import etree

def xml_to_pdf(response_content):

    root = etree.fromstring(response_content)
    numero_recibo = root.find('.//numeroRecibo')
    print(numero_recibo.text)
    
    REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    input_file = os.path.join(REPORTS_DIR, 'Layout_GNRE.jrxml')
    output_file = os.path.join(REPORTS_DIR, numero_recibo.text)

    

    
    

    # Criar um arquivo temporário com o conteúdo XML
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.xml') as temp_file:
        temp_file.write(response_content)
        temp_file_path = temp_file.name

    pyreportjasper = PyReportJasper()
    pyreportjasper.config(
        input_file=input_file,
        output_file=output_file,
        output_formats=["pdf"],
        db_connection={
            'driver': 'xml',
            'data_file': temp_file_path,
            'xml_xpath': '/Envelope/Body/gnreRespostaMsg/TResultLote_GNRE/resultado/guia',
        }
    )
    pyreportjasper.process_report()

    # Remover o arquivo temporário após o processamento
    os.remove(temp_file_path)

    print('Result is the file below.')
    print(output_file + '.pdf')


