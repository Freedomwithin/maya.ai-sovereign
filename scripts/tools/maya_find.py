import socket
import json
import sys

def query_memory(query):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 5555))
            s.sendall(query.encode())
            data = s.recv(4096)
            return json.loads(data.decode())
    except Exception as e:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: maya-find <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    results = query_memory(query)
    
    if not results:
        print("❌ Memory Daemon offline or no results found.")
    else:
        print(f"\n--- SOVEREIGN RECALL: '{query}' ---")
        for r in results:
            print(f"📍 [{r['Category'].upper()}] {r['Title']}")
            print(f"   Path: {r['Path']}")
            print(f"   Last Modified: {r['LastModified']}\n")
