from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
import os

def generate_pem_files(pfx_filename, password):
    
    try:
        # Ler o conteúdo do arquivo .pfx
        with open(pfx_filename, "rb") as f:
            pfx_data = f.read()

        # Carregar chave privada, certificado e cadeia de certificados
        private_key, certificate, _ = load_key_and_certificates(
            pfx_data, password.encode()
        )

        # Salvar a chave privada em key.pem
        with open("certificados/chave_certificado.pem", "wb") as key_file:
            key_file.write(private_key.private_bytes(
                Encoding.PEM,
                PrivateFormat.TraditionalOpenSSL,
                NoEncryption()
            ))

        # Salvar o certificado em cert.pem
        with open("certificados/certificado.pem", "wb") as cert_file:
            cert_file.write(certificate.public_bytes(Encoding.PEM))

        print("Arquivos chave_certificado.pem e certificado.pem gerados com sucesso!")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{pfx_filename}' não encontrado. Verifique o caminho.")
    except Exception as e:
        print(f"Erro ao processar o arquivo .pfx: {e}")

# Exemplo de uso
if __name__ == "__main__":
    # Nome do arquivo .pfx e senha
    pfx_filename = "certificados/certificado.pfx"  # Atualize com o nome correto do arquivo
    password = "senha_do_seu_certificado"   # Atualize com a senha correta

    generate_pem_files(pfx_filename, password)
