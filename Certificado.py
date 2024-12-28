
import os
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, NoEncryption
from cryptography.hazmat.primitives.serialization import PrivateFormat
from cryptography.hazmat.backends import default_backend
from certificados.empresas import EMPRESAS
# Diretório onde os arquivos PFX estão localizados
DIRETORIO_CERTIFICADOS = "certificados"



def certificadoA4(empresa):

    # Verifica se a chave da empresa existe no dicionário
    if empresa not in EMPRESAS:
        print(f"Empresa {empresa} não encontrada.")
        return None, None

    # Acessa o nome do arquivo PFX e a senha diretamente
    nome_pfx, senha = EMPRESAS[empresa]

    # Constrói o caminho completo para o arquivo PFX
    pfx_path = os.path.join(DIRETORIO_CERTIFICADOS, nome_pfx)

    try:
        # Lê o arquivo PFX
        with open(pfx_path, "rb") as pfx_file:
            pfx_data = pfx_file.read()

        # Carrega o conteúdo PFX usando cryptography
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            pfx_data,
            senha.encode(),
            backend=default_backend()
        )

        if private_key is None or certificate is None:
            raise ValueError("O arquivo PFX não contém chave privada ou certificado.")

        # Obtém a data de validade do certificado 
        data_validade = certificate.not_valid_after 
        # Formata a data de validade no formato ddmmaaaa 
        data_validade_formatada = data_validade.strftime("%d-%m-%Y")

        # Caminhos para os arquivos PEM
        certificado = os.path.join(DIRETORIO_CERTIFICADOS, f"{empresa}_VALIDO_ATE_{data_validade_formatada}_cert.pem")
        chave_certificado = os.path.join(DIRETORIO_CERTIFICADOS, f"{empresa}_VALIDO_ATE_{data_validade_formatada}_key.pem")

        # Verifica se os arquivos PEM já existem
        if os.path.exists(certificado) and os.path.exists(chave_certificado):
            return certificado, chave_certificado

        # Converte a chave privada para PEM
        key_pem = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )

        # Converte o certificado para PEM
        cert_pem = certificate.public_bytes(encoding=Encoding.PEM)

        # Salva os arquivos PEM
        with open(certificado, "wb") as cert_file:
            cert_file.write(cert_pem)

        with open(chave_certificado, "wb") as key_file:
            key_file.write(key_pem)

        return certificado, chave_certificado

    except Exception as e:
        print(f"Erro ao processar o arquivo PFX: {e}")
        return None, None


