import os
import ipaddress
from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Configurações
CERTS_DIR = "certs"
KEY_SIZE = 2048
VALIDITY_DAYS = 365

def save_key(key, filename):
    path = os.path.join(CERTS_DIR, filename)
    with open(path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    print(f"[OK] Chave salva: {path}")

def save_cert(cert, filename):
    path = os.path.join(CERTS_DIR, filename)
    with open(path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"[OK] Certificado salvo: {path}")

def generate_ca():
    """Gera a Autoridade Certificadora (CA) Raiz"""
    print("--- Gerando Autoridade Certificadora (CA) ---")
    key = rsa.generate_private_key(public_exponent=65537, key_size=KEY_SIZE)
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UnB - Trabalho Seguranca"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"WhatsChat Root CA"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=VALIDITY_DAYS)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).sign(key, hashes.SHA256())
    
    save_key(key, "ca-key.pem")
    save_cert(cert, "ca-cert.pem")
    return key, cert

def generate_server_cert(ca_key, ca_cert):
    """Gera o Certificado do Servidor assinado pela CA"""
    print("\n--- Gerando Certificado do Servidor (localhost) ---")
    key = rsa.generate_private_key(public_exponent=65537, key_size=KEY_SIZE)
    
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"BR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UnB"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    san = x509.SubjectAlternativeName([
        x509.DNSName(u"localhost"),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
        x509.IPAddress(ipaddress.ip_address("0.0.0.0"))
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=VALIDITY_DAYS)
    ).add_extension(
        san, critical=False
    ).sign(ca_key, hashes.SHA256())
    
    save_key(key, "server-key.pem")
    save_cert(cert, "server-cert.pem")

if __name__ == "__main__":
    if not os.path.exists(CERTS_DIR):
        os.makedirs(CERTS_DIR)
    
    # 1. Gera a CA
    ca_key, ca_cert = generate_ca()
    
    # 2. Gera o certificado do servidor usando a CA
    generate_server_cert(ca_key, ca_cert)
    
    print("\nCertificados gerados na pasta \"certs/\"!")