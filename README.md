# Slideshare-Downloader

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)

Slideshare Downloader é uma ferramenta de linha de comando em Python para baixar apresentações do [SlideShare](https://slideshare.net/) diretamente como arquivos PDF de alta qualidade.

O script automatiza todo o processo: acessa o link, extrai as imagens de cada slide na maior resolução disponível, remove as bordas/faixas brancas de cada imagem e, finalmente, compila tudo em um único arquivo PDF, nomeado com o título original da apresentação.

## Funcionalidades

-   **Download de Alta Qualidade**: Extrai a URL da imagem de maior resolução de cada slide.
-   **Saída em PDF Limpo**: Remove automaticamente as barras brancas ou de cor sólida das bordas de cada imagem antes de gerar o PDF.
-   **Suporte a Múltiplos Links**: Baixe várias apresentações de uma só vez, passando múltiplos links como argumento.
-   **Nomenclatura Inteligente**: Salva o arquivo PDF com o título original da apresentação.
-   **Flexível**: Funciona com diferentes domínios do SlideShare (ex: `slideshare.net`, `pt.slideshare.net`, etc.).

## Pré-requisitos

-   [Python 3.7+](https://www.python.org/downloads/)

## Instalação

1.  Clone este repositório para a sua máquina local:
    ```bash
    git clone https://github.com/etoshy/Slideshare-Downloader.git
    ```

2.  Navegue até a pasta do projeto:
    ```bash
    cd Slideshare-Downloader
    ```

3.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```
    *(O arquivo `requirements.txt` contém todas as bibliotecas que o script precisa para rodar).*

## Como Usar

O script é executado diretamente do seu terminal. A sintaxe básica é:

```
python slidedownload.py <URL1> <URL2> ...
```

#### Exemplo com um único link:

```bash
python slidedownload.py https://www.slideshare.net/lorenakamilamelo/fisiologia-humana-7-sistema-respiratorio
```

#### Exemplo com múltiplos links (separados por espaço):

```bash
python slidedownload.py https://link/da/apresentacao1 https://link/da/apresentacao2
```

O script irá processar cada link sequencialmente, criando um arquivo PDF para cada um na mesma pasta onde o script foi executado.

## Como Funciona

1.  **Acesso à URL**: O script acessa a versão mobile da URL do SlideShare, que possui uma estrutura HTML mais simples.
2.  **Análise do HTML**: Utiliza `BeautifulSoup` para analisar o conteúdo da página e encontrar o título da apresentação e as tags de imagem de cada slide.
3.  **Extração da Melhor Imagem**: Para cada slide, ele lê o atributo `srcset` e pega a URL da imagem de maior resolução.
4.  **Download e Limpeza**: Baixa cada imagem e a processa com a biblioteca `Pillow` para detectar e cortar as bordas brancas.
5.  **Criação do PDF**: Utiliza a biblioteca `img2pdf` para combinar as imagens limpas em um único arquivo PDF, garantindo que cada página tenha o tamanho exato da sua respectiva imagem (sem bordas adicionais).
6.  **Finalização**: Salva o arquivo PDF no seu computador.

## Autor

Desenvolvido por [**Etoshy**](https://github.com/etoshy).
