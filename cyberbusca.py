import os
import sys
import json
import base64
import re
import requests
from colorama import Fore, Back, Style, init

# Inicializa o colorama para compatibilidade universal de cores (Termux, PC, etc)
init(autoreset=True)

BASE_DOMAIN = "http://apisbrasilpro.site"

# Estrutura limpa mapeando o que o usuário realmente deseja buscar
OPCOES_BUSCA = {
    "1": {
        "nome": "Consultar por CPF",
        "url": f"{BASE_DOMAIN}/api_full.php",
        "param": "cpf",
        "label": "o CPF"
    },
    "2": {
        "nome": "Consultar por Nome",
        "url": f"{BASE_DOMAIN}/credilink.php",
        "param": "nome",
        "label": "o Nome Completo"
    },
    "3": {
        "nome": "Consultar por E-mail",
        "url": f"{BASE_DOMAIN}/api_full.php",
        "param": "email",
        "label": "o E-mail"
    },
    "4": {
        "nome": "Consultar por Telefone",
        "url": f"{BASE_DOMAIN}/api_full.php",
        "param": "telefone",
        "label": "o Telefone com DDD"
    },
    "5": {
        "nome": "Consultar por Placa",
        "url": f"{BASE_DOMAIN}/api_full.php",
        "param": "placa",
        "label": "a Placa do Veículo"
    },
    "6": {
        "nome": "Consultar por CEP",
        "url": f"{BASE_DOMAIN}/api_full.php",
        "param": "cep",
        "label": "o CEP"
    },
    "7": {
        "nome": "Consultar por Nome da Mãe",
        "url": f"{BASE_DOMAIN}/credilink.php",
        "param": "nome_mae",
        "label": "o Nome da Mãe"
    },
    "8": {
        "nome": "Buscar Foto pelo CPF (foto03)",
        "url": f"{BASE_DOMAIN}/foto03.php",
        "param": "id",
        "label": "o CPF para a Foto"
    },
    "9": {
        "nome": "Buscar Foto pelo CPF (foto06)",
        "url": f"{BASE_DOMAIN}/foto06.php",
        "param": "id",
        "label": "o CPF para a Foto"
    },
    "10": {
        "nome": "Buscar Foto pelo CPF (foto07)",
        "url": f"{BASE_DOMAIN}/foto07.php",
        "param": "id",
        "label": "o CPF para a Foto"
    },
    "11": {
        "nome": "Buscar Foto pelo CPF (foto08)",
        "url": f"{BASE_DOMAIN}/foto08.php",
        "param": "id",
        "label": "o CPF para a Foto"
    },
    "12": {
        "nome": "Consultar RAIS 2019",
        "url": f"{BASE_DOMAIN}/rais2019.php",
        "param": "cpf",
        "label": "o CPF para a RAIS"
    }
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.GREEN + "==============================================================")
    print(Fore.YELLOW + " [>] Painel de Consultas CyberBusca")
    print(Fore.YELLOW + " [>] made by elitexsp4m")
    print(Fore.GREEN + "==============================================================\n")

def exibir_dados_limpos(texto_bruto):
    """Filtra o retorno bruto e mostra as linhas de dados limpas de forma legível."""
    texto = str(texto_bruto)
    
    # Captura "CHAVE": "VALOR" ignorando escapes ruins da API
    padrao = r'(?:\\+["\']|["\'])([A-Za-zA-Z0-9_\s\-]+)(?:\\+["\']|["\'])\s*:\s*(?:\\+["\']|["\']|)([^"\'\\,{}]+)(?:\\+["\']|["\']|)'
    matches = re.findall(padrao, texto)
    
    if not matches:
        return False
        
    chaves_para_esconder = [
        "STATUS", "COUNT", "TOTAL", "MESSAGE", "MENSAGEM", "CONTEUDO", 
        "TEXTO", "TIPO", "LIMIT", "TABELA", "PARAMETRO_BUSCADO", "VALOR_BUSCADO", "ERRO", "IMAGEM"
    ]
    
    dados_encontrados = {}
    for chave, valor in matches:
        ch = chave.strip().upper()
        vl = valor.strip().replace(r'\/', '/').replace('\\', '')
        
        if ch not in chaves_para_esconder:
            if vl and vl.lower() != 'null' and vl.lower() != '[]':
                dados_encontrados[ch] = vl

    if dados_encontrados:
        print(Fore.CYAN + f"\n[+] Resultado da Busca:")
        print(Fore.MAGENTA + f"--------------------------------------------------------------")
        for chave, valor in dados_encontrados.items():
            print(Fore.GREEN + f" {chave}: " + Fore.WHITE + f"{valor}")
        print(Fore.MAGENTA + f"--------------------------------------------------------------")
        return True
        
    return False

def extrair_e_salvar_foto(texto_bruto, id_busca):
    """Verifica se há foto em Base64 no retorno e oferece o download."""
    texto = str(texto_bruto)
    # Procura pelo campo de imagem
    match = re.search(r'(?:\\+["\']|["\'])imagem(?:\\+["\']|["\'])\s*:\s*(?:\\+["\']|["\']|)([^"\'\\,{}]+)', texto)
    
    if match:
        img_b64 = match.group(1).strip().replace("\n", "").replace("\r", "").strip()
        if img_b64 and img_b64.lower() != 'null':
            print(Fore.GREEN + "\n[+] Uma foto foi localizada no retorno desta consulta!")
            print(Fore.YELLOW + "[?] Deseja baixar o arquivo da foto agora? (s/n): ", end="")
            if input().strip().lower() == 's':
                try:
                    missing_padding = len(img_b64) % 4
                    if missing_padding:
                        img_b64 += '=' * (4 - missing_padding)
                        
                    img_data = base64.b64decode(img_b64)
                    nome_foto = f"foto_{id_busca}.jpg"
                    with open(nome_foto, "wb") as f:
                        f.write(img_data)
                    print(Fore.GREEN + f"[+] Sucesso! Foto salva como: {nome_foto}")
                except Exception as e:
                    print(Fore.RED + f"[-] Não foi possível gerar o arquivo da foto: {e}")

def salvar_relatorio_texto(tipo_busca, valor_buscado, texto_bruto):
    """Oferece o download da resposta em arquivo de texto simples."""
    print(Fore.YELLOW + "\n[?] Deseja baixar o resultado em um arquivo de texto? (s/n): ", end="")
    if input().strip().lower() == 's':
        nome_arquivo = f"resultado_{tipo_busca}_{valor_buscado}.txt".replace(" ", "_")
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"=== CYBERBUSCA - RESULTADO DA CONSULTA ===\n")
                f.write(f"Tipo de Consulta: {tipo_busca}\n")
                f.write(f"Dado Pesquisado: {valor_buscado}\n")
                f.write(f"{'='*50}\n\n")
                f.write(str(texto_bruto))
            print(Fore.GREEN + f"[+] Arquivo de texto baixado com sucesso: {nome_arquivo}")
        except Exception as e:
            print(Fore.RED + f"[-] Erro ao salvar o arquivo: {e}")

def realizar_consulta(url, param_name, valor):
    print(Fore.CYAN + f"\n[*] Buscando informações no sistema, aguarde...")
    try:
        response = requests.get(url, params={param_name: valor}, timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            return f"Servidor indisponível no momento. Código: {response.status_code}"
    except Exception as e:
        return f"Não foi possível conectar ao servidor. Verifique sua conexão. Detalhes: {e}"

def menu_principal():
    while True:
        limpar_tela()
        banner()
        
        print(Fore.WHITE + " Escolha o que você deseja pesquisar:\n")
        for chave, info in OPCOES_BUSCA.items():
            # Alinha os números de 1 a 9 com os de 10 a 12 visualmente
            num_exibir = f"[{chave}]" if int(chave) >= 10 else f"[{chave}] "
            print(Fore.GREEN + f"  {num_exibir} " + Fore.WHITE + f"{info['nome']}")
        print(Fore.RED + "  [0]   Sair do Painel\n")
        
        opcao = input(Fore.YELLOW + " CyberBusca > ").strip()
        
        if opcao == "0":
            print(Fore.CYAN + "\n[*] Fechando o CyberBusca. Até mais!")
            sys.exit(0)
            
        if opcao in OPCOES_BUSCA:
            busca_selecionada = OPCOES_BUSCA[opcao]
            
            limpar_tela()
            banner()
            print(Fore.CYAN + f" Opção Selecionada: {busca_selecionada['nome']}\n")
            
            print(Fore.YELLOW + f"[?] Digite {busca_selecionada['label']}: ", end="")
            valor_busca = input().strip()
            
            if not valor_busca:
                print(Fore.RED + "\n[-] Você não digitou nada. Pressione ENTER para voltar...")
                input()
                continue
                
            # Executa a busca real
            resposta_servidor = realizar_consulta(busca_selecionada['url'], busca_selecionada['param'], valor_busca)
            
            # Tenta filtrar e exibir como lista limpa
            print(Fore.GREEN + f"\n{'='*25} RETORNO DO SISTEMA {'='*25}")
            exibiu_com_sucesso = exibir_dados_limpos(resposta_servidor)
            
            if not exibiu_com_sucesso:
                # Se não encontrar estrutura de dados válida ou der erro, mostra o texto puro recebido
                print(Fore.WHITE + str(resposta_servidor))
                
            print(Fore.GREEN + f"{'='*70}")
            
            # Se a resposta foi bem-sucedida ou trouxe dados, roda as opções de baixar
            if exibiu_com_sucesso or "success" in str(resposta_servidor).lower():
                extrair_e_salvar_foto(resposta_servidor, valor_busca)
                salvar_relatorio_texto(busca_selecionada['param'], valor_busca, resposta_servidor)
            
            print(Fore.YELLOW + "\nProcedimento concluído. Pressione ENTER para retornar ao menu principal...")
            input()
        else:
            print(Fore.RED + "\n[-] Opção inválida! Pressione ENTER para tentar novamente...")
            input()

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[-] Execução cancelada pelo usuário. Saindo do CyberBusca...")
        sys.exit(0)
