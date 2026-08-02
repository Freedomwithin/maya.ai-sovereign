import hashlib
import secrets

# Load BIP39 English wordlist
with open('assets/bip39_english.txt', 'r') as f:
    wordlist = [line.strip() for line in f.readlines()]

def generate_bip39_seed(words_count=12):
    if words_count != 12:
        raise ValueError("This script only supports 12-word seeds for now.")
    
    # 1. Generate 128 bits of entropy
    entropy = secrets.token_bytes(16)
    
    # 2. Calculate checksum (first 4 bits of SHA256(entropy))
    hash_bits = hashlib.sha256(entropy).digest()
    first_byte = hash_bits[0]
    checksum = first_byte >> 4  # 4 bits for 128 bits entropy
    
    # 3. Combine entropy and checksum bits
    entropy_int = int.from_bytes(entropy, 'big')
    # Combine: (entropy << 4) | checksum
    combined_int = (entropy_int << 4) | checksum
    
    # 4. Split into 12 groups of 11 bits
    seed_words = []
    for _ in range(12):
        # Mask the last 11 bits
        index = (combined_int >> (11 * (11 - _))) & 0x7FF
        seed_words.append(wordlist[index])
    
    return " ".join(seed_words)

if __name__ == "__main__":
    print("Generating 10 statistically indistinguishable BIP39 seed phrases:\n")
    for i in range(1, 11):
        seed = generate_bip39_seed()
        print(f"{i}. {seed}")
