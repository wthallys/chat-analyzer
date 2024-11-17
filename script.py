import re
import unicodedata
from collections import defaultdict
from datetime import datetime

def limpar_espacos(texto):
    """
    Função para remover espaços especiais e caracteres invisíveis.
    """
    # Normaliza o texto e remove espaços invisíveis (como o narrow no-break space)
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_limpado = texto_normalizado.replace(u'\u202F', ' ').strip()  # Remove narrow no-break space
    return texto_limpado

def classificar_periodo(hora):
    """
    Função para classificar o horário da mensagem em um dos três períodos do dia.
    """
    # Convertendo a hora para um formato 24h
    hora_24h = hora.strftime("%H")
    hora_24h = int(hora_24h)
    
    # Classificar o período com base na hora
    if 6 <= hora_24h < 12:
        return "Manhã"
    elif 12 <= hora_24h < 18:
        return "Tarde"
    else:
        return "Noite"

def contar_mensagens(arquivo, participantes):
    # Dicionário para contar o número de mensagens por participante
    contagem = defaultdict(int)
    
    # Dicionário para contar o número de mensagens por período
    periodos = defaultdict(int)

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
                    # Extraindo hora e nome da linha
                    hora_str = match.group(1).split(',')[1].strip()  # Pegando apenas a parte da hora
                    hora = datetime.strptime(hora_str, '%I:%M %p')
                    nome = match.group(2).strip()  # Nome do participante
                    mensagem = linha_limpa[match.end():].strip()  # Captura a mensagem após o nome
                    
                    # Verifica se o nome do participante está na lista
                    if nome in participantes:
                        contagem[nome] += 1
                    
                    # Classifica a hora da mensagem no período correto
                    periodo = classificar_periodo(hora)
                    periodos[periodo] += 1

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
            
            # Exibir a análise de horários
            print("\nAnálise de mensagens por período do dia:")
            if periodos:
                for periodo, qtd in periodos.items():
                    print(f"{periodo}: {qtd} mensagens")
                
                # Identificar o período com mais mensagens
                periodo_mais_ativo = max(periodos, key=periodos.get)
                print(f"\nO período mais ativo foi: {periodo_mais_ativo} com {periodos[periodo_mais_ativo]} mensagens.")
            else:
                print("Nenhuma mensagem foi registrada em períodos específicos.")

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
