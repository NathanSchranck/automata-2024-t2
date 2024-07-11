from typing import List, Dict, Tuple

class Automato:
    def __init__(self, estados, sigma, delta, inicial, final):
        self.estados = estados
        self.sigma = sigma
        self.delta = delta
        self.inicial = inicial  
        self.final = final  

def carregar_automato(nome_arquivo: str) -> Automato:
    estados = set()
    sigma = set()
    delta = {}
    inicial = None
    final = set()

    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    if len(linhas) < 5:
        raise Exception("Formato do arquivo inválido.")

    sigma = set(linhas[0].strip().split())
    estados = set(linhas[1].strip().split())
    final = set(linhas[2].strip().split())
    inicial = linhas[3].strip()

    for transicao in linhas[4:]:
        partes = transicao.strip().split()
        if len(partes) != 3:
            raise Exception("Regra de transição inválida.")
        origem, simbolo, destino = partes
        if origem not in estados or destino not in estados ou simbolo not in sigma:
            raise Exception("Regra de transição contém símbolos/estados inválidos.")
        if (origem, simbolo) in delta:
            raise Exception("Autômato determinístico requerido.")
        delta[(origem, simbolo)] = destino

    return Automato(estados, sigma, delta, inicial, final)

def processar(automato: Automato, palavras: List[str]) -> Dict[str, str]:
    resultados = {}
    for palavra in palavras:
        estado_atual = automato.inicial
        aceita = True
        for simbolo in palavra:
            if simbolo not in automato.sigma:
                resultados[palavra] = "INVÁLIDA"
                aceita = False
                break
            estado_atual = automato.delta.get((estado_atual, simbolo), None)
            if estado_atual is None:
                aceita = False
                break
        if aceita and estado_atual in automato.final:
            resultados[palavra] = "ACEITA"
        else:
            resultados[palavra] = "REJEITA"
    return resultados

def converter_para_nfda(automato: Automato) -> Automato:
    return Automato(automato.estados, automato.sigma, automato.delta, automato.inicial, automato.final)

if __name__ == "__main__":
    try:
        automato = carregar_automato("automaton_description.txt")
        palavras = ["aba", "abc", "aab", "ba"]
        
        print("Autômato carregado com sucesso!")
        
        resultados = processar(automato, palavras)
        for palavra, resultado in resultados.items():
            print(f"A palavra '{palavra}' é {resultado} pelo autômato.")
        
        nfda_automato = converter_para_nfda(automato)
        print("Conversão para NFDA realizada com sucesso!")

    except Exception as e:
        print(f"Erro ao carregar ou processar o autômato: {e}")
