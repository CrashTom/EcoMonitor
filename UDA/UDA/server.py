"""
EcoMonitor – server.py
Server TCP multithreading con coda condivisa.
"""
 
import socket
import threading
import queue
import csv
import os
from datetime import datetime
 
HOST = "0.0.0.0"
PORT = 5000
CSV_FILE = "misure.csv"
 
coda = queue.Queue()
coda_lock = threading.Lock()
coda_lista = []
 
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["studente", "sensore", "valore", "luogo", "data_ora"])
 
 
def salva_csv(studente, sensore, valore, luogo, data_ora):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([studente, sensore, valore, luogo, data_ora])
 
 
def gestisci_client(conn, addr):
    print(f"[CONNESSIONE] {addr}")
    studente = "sconosciuto"
    try:
        with conn:
            nome_raw = conn.recv(1024).decode("utf-8").strip()
            if nome_raw.startswith("NOME:"):
                studente = nome_raw[5:].strip()
            conn.sendall(f"Benvenuto {studente}!\n".encode("utf-8"))
 
            while True:
                dati = conn.recv(4096).decode("utf-8").strip()
                print(f"[DEBUG] ricevuto: {repr(dati)}")
 
                if not dati:
                    break
 
                if dati == "ESCI":
                    conn.sendall("Connessione chiusa.\n".encode("utf-8"))
                    break
 
                elif dati == "CODA":
                    with coda_lock:
                        if coda_lista:
                            risposta = "Coda attuale:\n" + "\n".join(
                                f"  {i+1}. {r}" for i, r in enumerate(coda_lista)
                            ) + "\n"
                        else:
                            risposta = "Coda vuota.\n"
                    conn.sendall(risposta.encode("utf-8"))
 
                elif dati.startswith("INVIA:"):
                    payload = dati[6:].strip()
                    parti = payload.split(",")
                    if len(parti) != 3:
                        conn.sendall(
                            "Errore: formato INVIA:sensore,valore,luogo\n".encode("utf-8")
                        )
                        continue
 
                    sensore, valore, luogo = (p.strip() for p in parti)
                    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
                    voce = f"{studente},{sensore},{valore},{luogo},{data_ora}"
                    with coda_lock:
                        coda_lista.append(voce)
                    coda.put(voce)
 
                    salva_csv(studente, sensore, valore, luogo, data_ora)
                    with coda_lock:
                        if voce in coda_lista:
                            coda_lista.remove(voce)
                    try:
                        coda.get_nowait()
                    except queue.Empty:
                        pass
 
                    risposta = f"OK | data_ora: {data_ora}\n"
                    conn.sendall(risposta.encode("utf-8"))
 
                else:
                    conn.sendall("Comando sconosciuto. Usa: INVIA, CODA, ESCI\n".encode("utf-8"))
 
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNESSO] {studente} ({addr})")
 
 
def avvia_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"[SERVER] In ascolto su {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=gestisci_client, args=(conn, addr), daemon=True)
            t.start()
            print(f"[THREAD ATTIVI] {threading.active_count() - 1}")
 
 
if __name__ == "__main__":
    avvia_server()