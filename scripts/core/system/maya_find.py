import socket
import json
import sys

def query_memory(query, folder_filter=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)  # Add timeout for reliability
            s.connect(("127.0.0.1", 5999))
            
            # Standardize payload as JSON for the C# backend to parse easily
            payload = json.dumps({"query": query, "folder": folder_filter})
            s.sendall(payload.encode('utf-8'))
            
            chunks = []
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
            
            raw_data = b"".join(chunks).decode('utf-8')
            if not raw_data:
                return None
            
            return json.loads(raw_data)
            
    except json.JSONDecodeError:
        print("Error: Received malformed JSON from daemon.")
        return None
    except ConnectionRefusedError:
        print("Error: Connection refused. Is the daemon running?")
        return None
    except socket.timeout:
        print("Error: Daemon request timed out.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: maya-find <query> [folder]")
        sys.exit(1)
    
    query_str = sys.argv[1]
    folder_filter = sys.argv[2] if len(sys.argv) > 2 else None
    
    results = query_memory(query_str, folder_filter)
    
    if results is None:
        print("❌ Memory Daemon offline or invalid response.")
    elif not results:
        print(f"🔍 No results found for '{query_str}'.")
    else:
        print(f"\n--- SOVEREIGN RECALL: '{query_str}' ---")
        for r in results:
            print(f"📍 [{r.get('Category', 'N/A').upper()}] {r.get('Title', 'Unknown')}")
            print(f"    Path: {r.get('Path', 'N/A')}")
            print(f"    Modified: {r.get('LastModified', 'N/A')}\n")