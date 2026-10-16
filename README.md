# CyberBusca

Puxa dados com o cpf,etc,dados de cartão,placa de carro/moto.

Painel de consultas em linha de comando para realizar buscas em diferentes endpoints definidos no script `cyberbusca.py`.

O script oferece um menu interativo que permite consultar diversos serviços (CPF, nome, e-mail, telefone, placa, CEP, nome da mãe, fotos associadas ao CPF e RAIS 2019) e fornece opções para salvar o resultado em arquivo texto e/ou salvar fotos retornadas em Base64.

---

## Sumário

- Funcionalidades
- Requisitos
- Instalação
- Uso (exemplos)
- Detalhes das opções de busca
- Arquivos gerados
- Personalização
- Autor

---

## Funcionalidades

- Menu interativo em terminal com opções de consulta.
- Requisições HTTP GET aos endpoints configurados no arquivo `cyberbusca.py`.
- Filtragem e exibição de pares chave/valor legíveis a partir do retorno bruto da API.
- Detecção de imagens codificadas em Base64 no campo `imagem` do retorno e opção de salvá-las como `foto_<id>.jpg`.
- Opção para salvar o retorno completo em `resultado_<tipo>_<valor>.txt`.

---

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - requests
  - colorama

Instale as dependências com:

```bash
pip install requests colorama
```

---

## Instalação

1. Clone o repositório ou baixe o arquivo `cyberbusca.py`:

```bash
git clone https://github.com/elitexspam/CyberBusca.git
cd CyberBusca
```

2. Instale as dependências (ver seção acima).

3. Execute o script:

```bash
python cyberbusca.py
# ou
python3 cyberbusca.py
```

O script inicia um menu interativo no terminal. Siga as instruções exibidas para escolher o tipo de consulta e fornecer o dado solicitado.

---

## Uso (exemplo)

Ao executar o script você verá um menu numerado. Exemplo de fluxo:

1. Execute: `python cyberbusca.py`
2. Escolha uma opção, por exemplo `1` para consultar por CPF.
3. Informe o CPF quando solicitado.
4. O script exibirá os dados retornados pela API (filtrados quando possível).
5. Caso haja uma foto no retorno, será oferecida a opção para salvá-la.
6. Também será perguntado se deseja salvar o resultado completo em um arquivo de texto.

---

## Detalhes das opções de busca

As opções estão definidas no dicionário `OPCOES_BUSCA` dentro de `cyberbusca.py`. Abaixo segue o mapeamento atual (domínio base configurado em `BASE_DOMAIN`):

1. Consultar por CPF — endpoint: `/api_full.php` (param: `cpf`)
2. Consultar por Nome — endpoint: `/credilink.php` (param: `nome`)
3. Consultar por E-mail — endpoint: `/api_full.php` (param: `email`)
4. Consultar por Telefone — endpoint: `/api_full.php` (param: `telefone`)
5. Consultar por Placa — endpoint: `/api_full.php` (param: `placa`)
6. Consultar por CEP — endpoint: `/api_full.php` (param: `cep`)
7. Consultar por Nome da Mãe — endpoint: `/credilink.php` (param: `nome_mae`)
8. Buscar Foto pelo CPF (foto03) — endpoint: `/foto03.php` (param: `id`)
9. Buscar Foto pelo CPF (foto06) — endpoint: `/foto06.php` (param: `id`)
10. Buscar Foto pelo CPF (foto07) — endpoint: `/foto07.php` (param: `id`)
11. Buscar Foto pelo CPF (foto08) — endpoint: `/foto08.php` (param: `id`)
12. Consultar RAIS 2019 — endpoint: `/rais2019.php` (param: `cpf`)

O domínio base usado no script é configurado na variável `BASE_DOMAIN` no topo do arquivo (valor atual no código: `http://apisbrasilpro.site`).

---

## Formato e arquivos gerados

- Fotos salvas: `foto_<valor>.jpg` (quando o campo `imagem` contiver Base64 e o usuário optar por salvar).
- Relatórios de texto: `resultado_<tipo>_<valor>.txt` — contém cabeçalho com tipo de consulta, dado pesquisado e o retorno bruto recebido.

---

## Como o script processa a resposta

- Faz uma requisição GET ao endpoint configurado com o parâmetro correspondente.
- Tenta extrair pares "CHAVE": "VALOR" do texto retornado usando expressões regulares e oculta campos de metadados comuns.
- Exibe os pares encontrados no terminal formatados com cores (via `colorama`).
- Se encontrar campo `imagem` com Base64, oferece salvamento da foto.

---

## Personalização

- Alterar o domínio/API: edite a variável `BASE_DOMAIN` no topo de `cyberbusca.py`.
- Adicionar/editar opções de busca: modifique o dicionário `OPCOES_BUSCA` para incluir novos endpoints, parâmetros e labels.
- Para uso não interativo ou automação, separe a função `realizar_consulta` e chame-a diretamente em outro script.

---

## Autor

Made by elitexsp4m (conforme banner no código)
