import re
import unicodedata
from collections import defaultdict

def limpar_espacos(texto):
    """
    Função para remover espaços especiais e caracteres invisíveis.
    """
    # Normaliza o texto e remove espaços invisíveis (como o narrow no-break space)
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_limpado = texto_normalizado.replace(u'\u202F', ' ').strip()  # Remove narrow no-break space
    return texto_limpado

def contar_mensagens(arquivo, participantes):
    # Dicionário para contar o número de mensagens por participante
    contagem = defaultdict(int)
    
    try:
        # Abrindo o arquivo .txt
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
            if not linhas:
                print("O arquivo está vazio ou não contém mensagens.")
                return

            for linha in linhas:
                # Limpar a linha para remover espaços especiais ou caracteres invisíveis
                linha_limpa = limpar_espacos(linha)

                # Verificando se a linha contém uma mensagem com a estrutura 'data, hora - nome: mensagem'
                match = re.match(r"(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [APM]{2}) - ([^:]+):", linha_limpa)
                
                if match:
                    nome = match.group(2).strip()  # Remove qualquer espaço extra no nome
                    mensagem = linha_limpa[match.end():].strip()  # Captura a mensagem após o nome
                    
                    # Se a mensagem for "Media omitted" ou similar, considera apenas como uma mensagem
                    if "Media omitted" in mensagem:
                        contagem[nome] += 1
                    else:
                        contagem[nome] += 1

            # Exibindo os resultados
            print("\nContagem de mensagens por participante:")
            if contagem:
                for participante, qtd in contagem.items():
                    print(f"{participante}: {qtd} mensagens")
                
                # Identificar o participante mais ativo
                participante_mais_ativo = max(contagem, key=contagem.get)
                print(f"\nO participante mais ativo foi: {participante_mais_ativo} com {contagem[participante_mais_ativo]} mensagens.")
            else:
                print("Nenhuma mensagem foi contada.")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Lista de participantes
participantes = ['nomes']

# Caminho para o arquivo de mensagens
arquivo = 'mensagens.txt'

# Chama a função para contar as mensagens
contar_mensagens(arquivo, participantes)