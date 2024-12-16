from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Replace this with your PEM-encoded private key
pem_key = """
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEICboG33Op4qBeDbKm2gmabjXhlJx8B8H6nHN9VOL8gL7oAoGCCqGSM49
AwEHoUQDQgAEIM3+eYhqdzeivqjIqnm+zkGEH+vmNEBRFDBKuCBODi3g7vXT6Y+T
XC9o2p+5dqIT48h/1h4Mgv2yHILP1JvICw==
-----END EC PRIVATE KEY-----
"""

# Load the PEM private key
private_key = serialization.load_pem_private_key(
    pem_key.encode(), password=None, backend=default_backend()
)

# Extract the raw private key bytes
private_key_hex = private_key.private_numbers().private_value.to_bytes(32, byteorder="big").hex()

print(f"Raw private key (hex): {private_key_hex}")
