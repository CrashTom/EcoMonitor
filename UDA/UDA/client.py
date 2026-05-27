"""
EcoMonitor – client.py
Client TCP interattivo.
Comandi: INVIA, CODA, ESCI
"""
 
import socket
 
HOST = "127.0.0.1"
PORT = 5000
 
def recv_risposta(s):
    """Legge la risposta del server fino a newline."""
    dati = b""
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        dati += chunk
        if b"\n" in dati:
            break
    return dati.decode("utf-8").strip()
 
def main():
    studente = input("Inserisci il tuo nome: ").strip()
    if not studente:
        print("Nome non valido.")
        return
 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
 
            # Invio del nome al server
            s.sendall(f"NOME:{studente}\n".encode("utf-8"))
            benvenuto = recv_risposta(s)
            print(f"[SERVER] {benvenuto}")
 
            print("\nComandi disponibili:")
            print("  INVIA  – invia una misura")
            print("  CODA   – mostra stato della coda")
            print("  ESCI   – chiudi la connessione\n")
 
            while True:
                cmd = input("Comando> ").strip().upper()
 
                if cmd == "ESCI":
                    s.sendall(b"ESCI\n")
                    risposta = recv_risposta(s)
                    print(f"[SERVER] {risposta}")
                    break
 
                elif cmd == "CODA":
                    s.sendall(b"CODA\n")
                    risposta = recv_risposta(s)
                    print(f"[SERVER] {risposta}")
 
                elif cmd == "INVIA":
                    sensore = input("  Sensore (es. luce): ").strip()
                    valore  = input("  Valore misurato: ").strip()
                    luogo   = input("  Luogo (es. aula_4A): ").strip()
 
                    if not sensore or not valore or not luogo:
                        print("  Tutti i campi sono obbligatori.")
                        continue
 
                    s.sendall(f"INVIA:{sensore},{valore},{luogo}\n".encode("utf-8"))
                    risposta = recv_risposta(s)
                    print(f"[SERVER] {risposta}")
 
                else:
                    print("Comando non riconosciuto. Usa: INVIA, CODA, ESCI")
 
    except ConnectionRefusedError:
        print("Errore: impossibile connettersi al server. Hai avviato server.py?")
    except Exception as e:
        print(f"Errore: {e}")
 
if __name__ == "__main__":
    main()