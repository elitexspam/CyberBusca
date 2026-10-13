import os
import sys
import json
import base64
import requests
from colorama import Fore, Back, Style, init

# Inicializa o colorama para compatibilidade universal de cores (Termux, PC, etc)
init(autoreset=True)

# Estrutura de menus baseada puramente nos endpoints reais fornecidos por você
APIS = {
    "1": {
        "nome": "Credilink (Consultas Gerais)",
        "base_url": "http://apisbrasilpro.site/credilink.php?",
        "params": ["cpf", "nome", "email", "nome_mae", "cep"]
    },
    "2": {
        "nome": "Busca de Fotos (Identidades/Cadastros)",
        "base_url": "http://apisbrasilpro.site/foto03.php?", # Rota principal enviada
        "params": ["id"],
        "alternativas": {
            "06": "http://apisbrasilpro.site/foto06.php?",
            "07": "http://apisbrasilpro.site/foto07.php?",
            "08": "http://apisbrasilpro.site/foto08.php?"
        }
    },
    "3": {
        "nome": "RAIS 2019",
        "base_url": "http://apisbrasilpro.site/rais2019.php?",
        "params": ["cpf"]
    },
    "4": {
        "nome": "API Full (Dados Completos)",
        "base_url": "http://apisbrasilpro.site/api_full.php?",
        "params": ["cep", "email", "placa", "telefone", "cpf"]
    }
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""Fore.CYAN + Style.BRIGHT + rr""")
  _________コイル__________ _________                                  
  \_   ___ \_   _  \______   \\______   \__ __  ______ ____ _____   
  /    \  \//  /_\  \|    |  _/ |    |  _/  |  \/  ___// ___\\__  \  
  \     \___\  \_/   \    |   \ |    |   \  |  /\___ \\  \___ / __ \_
   \______  /\_____  /______  /______  /____//____  >\___  >____  /
          \/       \/       \/       \/           \/     \/     \/ 
    """)
    print(Fore.GREEN + f" {'='*62}")
    print(Fore.YELLOW + f" [>] Painel de Consultas Avançado: CyberBusca")
    print(Fore.YELLOW + f" [>] API desenvolvida por @astrahvhdev telegram")
    print(Fore.GREEN + f" {'='*62}\n")

def realizar_requisicao(url, param_name, valor):
    """Realiza a chamada HTTP real para o endpoint privado."""
    print(Fore.CYAN + f"\n[*] Enviando requisição para o servidor privado...")
    try:
        # Envia os parâmetros no formato exato que o PHP espera (?cpf=valor, ?id=valor, etc)
        response = requests.get(url, params={param_name: valor}, timeout=20)
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                # Caso o servidor retorne texto puro ou erro de estrutura
                return {"erro": True, "mensagem": "A API não retornou um JSON válido.", "resposta_bruta": response.text}
        else:
            return {"erro": True, "mensagem": f"Erro de conexão com o servidor. Status: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"erro": True, "mensagem": f"Falha na rede ou timeout ao conectar: {e}"}

def processar_foto(dados, id_consultado):
    """Varre a resposta JSON real em busca da imagem em Base64 para download."""
    if isinstance(dados, dict) and "dados" in dados:
        for item in dados["dados"]:
            if "imagem" in item and item["imagem"]:
                print(Fore.GREEN + "\n[+] Uma imagem em Base64 foi localizada no retorno desta API!")
                print(Fore.YELLOW + "[?] Deseja decodificar e baixar a foto agora? (s/n): ", end="")
                if input().strip().lower() == 's':
                    try:
                        # Limpa espaços ou quebras de linha comuns em strings Base64 longas
                        img_b64 = item["imagem"].replace("\n", "").replace("\r", "").strip()
                        
                        # Corrige problemas de padding automático do Base64 caso necessário
                        missing_padding = len(img_b64) % 4
                        if missing_padding:
                            img_b64 += '=' * (4 - missing_padding)
                            
                        img_data = base64.b64decode(img_b64)
                        nome_foto = f"foto_{id_consultado}.jpg"
                        
                        with open(nome_foto, "wb") as f:
                            f.write(img_data)
                        print(Fore.GREEN + f"[+] Sucesso! Imagem salva no seu diretório como: {nome_foto}")
                    except Exception as e:
                        print(Fore.RED + f"[-] Falha crítica ao decodificar/salvar a imagem: {e}")

def salvar_resultado(tipo_busca, parametro, dados):
    """Gerencia o salvamento dos logs de resposta em formato de arquivo de texto."""
    print(Fore.YELLOW + "\n[?] Deseja salvar e baixar o relatório de texto desta consulta? (s/n): ", end="")
    opcao = input().strip().lower()
    
    if opcao == 's':
        nome_arquivo = f"resultado_{tipo_busca}_{parametro}.txt".replace(" ", "_")
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"=== CYBERBUSCA - RELATÓRIO DE CONSULTA ===\n")
                f.write(f"Módulo de Consulta: {tipo_busca}\n")
                f.write(f"Filtro Utilizado: {parametro}\n")
                f.write(f"{'='*50}\n\n")
                f.write(json.dumps(dados, indent=4, ensure_ascii=False))
            print(Fore.GREEN + f"[+] Relatório de texto baixado com sucesso: {nome_arquivo}")
        except Exception as e:
            print(Fore.RED + f"[-] Erro ao gravar o arquivo de log: {e}")
    else:
        print(Fore.CYAN + "[*] Download do texto ignorado.")

def menu_principal():
    while True:
        limpar_tela()
        banner()
        
        print(Fore.WHITE + " Selecione o Banco de Dados/Módulo desejado:\n")
        for chave, info in APIS.items():
            print(Fore.GREEN + f"  [{chave}] " + Fore.WHITE + f"{info['nome']}")
        print(Fore.RED + "  [0] Sair do CyberBusca\n")
        
        opcao = input(Fore.YELLOW + " CyberBusca > ").strip()
        
        if opcao == "0":
            print(Fore.CYAN + "\n[*] Desconectando do painel CyberBusca. Até logo!")
            sys.exit(0)
            
        if opcao in APIS:
            menu_parametros(APIS[opcao])
        else:
            print(Fore.RED + "\n[-] Opção inválida! Pressione ENTER para tentar novamente...")
            input()

def menu_parametros(api):
    while True:
        limpar_tela()
        banner()
        print(Fore.CYAN + f" Módulo Ativo: {api['nome']}\n")
        print(Fore.WHITE + " Escolha a rota de parâmetro correspondente no PHP:")
        
        for idx, param in enumerate(api['params'], 1):
            print(Fore.GREEN + f"  [{idx}] " + Fore.WHITE + f"Consultar por ?{param}=")
            
        # Adiciona tratamento visual para as fotos alternativas (06, 07, 08) se for o módulo de foto
        if "alternativas" in api:
            print(Fore.GREEN + f"  [6] " + Fore.WHITE + "Consultar Foto via rota foto06.php")
            print(Fore.GREEN + f"  [7] " + Fore.WHITE + "Consultar Foto via rota foto07.php")
            print(Fore.GREEN + f"  [8] " + Fore.WHITE + "Consultar Foto via rota foto08.php")
            
        print(Fore.RED + "  [0] Voltar ao Menu Principal\n")
        
        sub_opcao = input(Fore.YELLOW + f" CyberBusca -> {api['nome']} > ").strip()
        
        if sub_opcao == "0":
            break
            
        url_alvo = api['base_url']
        parametro_php = ""
        
        # Lógica especial para as sub-rotas de fotos (06, 07, 08)
        if "alternativas" in api and sub_opcao in ["6", "7", "8"]:
            chave_alt = f"0{sub_opcao}" if sub_opcao != "0" else ""
            url_alvo = api['alternativas'][chave_alt]
            parametro_php = "id"
        else:
            try:
                idx_escolhido = int(sub_opcao) - 1
                if 0 <= idx_escolhido < len(api['params']):
                    parametro_php = api['params'][idx_escolhido]
                else:
                    print(Fore.RED + "[-] Opção inválida! Pressione ENTER...")
                    input()
                    continue
            except ValueError:
                print(Fore.RED + "[-] Entrada inválida! Digite apenas números. Pressione ENTER...")
                input()
                continue

        print(Fore.YELLOW + f"\n[?] Digite o valor para o parâmetro '{parametro_php}': ", end="")
        valor_busca = input().strip()
        
        # Realiza a consulta HTTP real usando os endpoints informados
        resultado = realizar_requisicao(url_alvo, parametro_php, valor_busca)
        
        # Exibe a resposta estruturada diretamente na tela do terminal
        print(Fore.GREEN + f"\n{'='*25} RETORNO DA API SEGURO {'='*25}")
        print(Fore.WHITE + json.dumps(resultado, indent=4, ensure_ascii=False))
        print(Fore.GREEN + f"{'='*72}")
        
        # Executa as verificações de download se a requisição não falhou estruturalmente
        if isinstance(resultado, dict) and not resultado.get("erro", False) or "dados" in resultado:
            processar_foto(resultado, valor_busca)
            salvar_resultado(api['nome'], valor_busca, resultado)
        else:
            print(Fore.RED + "\n[-] A resposta retornou erros ou não possui registros válidos para download.")
            
        print(Fore.YELLOW + "\nConsulta concluída. Pressione ENTER para continuar...")
        input()

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[-] Conexão abortada pelo usuário. Saindo do CyberBusca...")
        sys.exit(0)
        