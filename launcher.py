import requests
import os
import subprocess

# Configurações do seu GitHub
URL_VERSAO = "https://github.com/gustavodedeus111-ctrl/ver_atualizacao/blob/main/version.txt"
#URL_JOGO = "https://raw.githubusercontent.com/SEU_USER/SEU_REPO/main/main.py"

def atualizar_e_abrir():
    print("Verificando atualizações...")
    try:
        # 1. Pega a versão remota
        v_remota = requests.get(URL_VERSAO).text.strip()
        
        # 2. Lê a versão local (se não existir, assume que precisa baixar)
        v_local = "0"
        if os.path.exists("version.txt"):
            with open("version.txt", "r") as f:
                v_local = f.read().strip()

        # 3. Se for diferente, baixa o novo arquivo
        if v_remota != v_local:
            print(f"Atualizando da v{v_local} para v{v_remota}...")
            #novo_codigo = requests.get(URL_JOGO).content
            
           # with open("main.py", "wb") as f:
               # f.write(novo_codigo)
            
           # with open("version.txt", "w") as f:
               # f.write(v_remota)
           # print("Atualização concluída!")

    except Exception as e:
        print(f"Não foi possível atualizar (jogando offline): {e}")

    # 4. Abre o jogo (se for .exe, mude para main.exe)
    print("Iniciando o jogo...")
    subprocess.Popen(["python", "main.py"]) 

if __name__ == "__main__":
    atualizar_e_abrir()