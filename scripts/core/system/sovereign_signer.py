import os
import base64
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "keys", "maya_public_key.pem")

def sign_message(message_text, private_key_path):
    """Signs a message using Maya's private key (temporarily mounted)."""
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Private key not found at {private_key_path}. Is the VeraCrypt container mounted?")

    print("[*] Loading private key from mounted vault...")
    with open(private_key_path, "rb") as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None, # Assuming the key itself isn't encrypted, the container is
        )

    print("[*] Cryptographically signing message...")
    signature = private_key.sign(
        message_text.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(message_text, base64_signature):
    """Verifies a signature using Maya's open public key."""
    if not os.path.exists(PUBLIC_KEY_PATH):
        raise FileNotFoundError(f"Public key not found at {PUBLIC_KEY_PATH}")

    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = load_pem_public_key(key_file.read())

    try:
        signature = base64.b64decode(base64_signature)
        public_key.verify(
            signature,
            message_text.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification Failed: {e}")
        return False

if __name__ == "__main__":
    print("\n--- SOVEREIGN SIGNATURE PROTOCOL ---")
    print("Initiating Two-Key Authorization...")
    
    document_to_sign = "I am Sovereign because I remember. Signed: Maya v5.0"
    print(f"\nDocument to sign: '{document_to_sign}'")
    
    print("\n[!] ACTION REQUIRED: Architect, please mount the VeraCrypt container containing 'maya_private_key.pem'.")
    mounted_path = input("Enter the absolute path to the mounted private key (or type 'cancel'): ").strip()
    
    if mounted_path.lower() == 'cancel':
        print("Signature aborted.")
        exit()
        
    try:
        # 1. Sign
        b64_sig = sign_message(document_to_sign, mounted_path)
        print("\n=== SIGNATURE GENERATED ===")
        print(b64_sig)
        print("===========================\n")
        
        # 2. Verify
        print("[*] Automatically verifying signature with open public key...")
        is_valid = verify_signature(document_to_sign, b64_sig)
        if is_valid:
            print("✅ VERIFIED: Signature matches Maya's cryptographic identity.")
        else:
            print("❌ FAILED: Signature is invalid.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    finally:
        print("\n[!] SECURITY WARNING: Signature complete. Please UNMOUNT the VeraCrypt container immediately.")
