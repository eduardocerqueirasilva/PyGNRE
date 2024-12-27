# -*- coding: utf-8 -*-
import os
import tempfile
from pyreportjasper import PyReportJasper
from lxml import etree
import base64

def xml_to_pdf(response_content, to_base64=False, nome="GNRE"):
    if to_base64:
        root = etree.fromstring(response_content)
        ns = {'ns': 'http://www.gnre.pe.gov.br'}
        pdf_guias = root.find('.//pdfGuias')
        
        if pdf_guias is not None and pdf_guias.text:
            pdf_content = base64.b64decode(pdf_guias.text)
            pdf_file_path = f'reports/{nome}.pdf'
            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)
            print("PDF salvo como gnre2.pdf")
            return pdf_file_path
        else:
            print("pdfGuias não encontrado na resposta.")
            return None
    else:
        root = etree.fromstring(response_content)
        numero_recibo = root.find('.//numeroRecibo')
        print(numero_recibo.text)
        
        REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
        input_file = os.path.join(REPORTS_DIR, 'Layout_GNRE.jrxml')
        output_file = os.path.join(REPORTS_DIR, f'{nome}')
    

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

        pdf_file_path = output_file + '.pdf'
        print('Result is the file below.')
        print(pdf_file_path)
        return pdf_file_path


