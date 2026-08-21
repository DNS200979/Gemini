import os
import sys
import google.generativeai as genai

# Configura a API usando a variável de ambiente
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def gerar_arquivo(nome_arquivo, prompt):
    # Usa o modelo mais rápido e eficiente para tarefas de código
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Instrução de sistema forçando o modelo a retornar APENAS o código
    instrucao = f"Escreva o código para a seguinte solicitação: '{prompt}'. Retorne APENAS o código limpo, sem explicações em texto e sem blocos de formatação markdown (como ```python)."
    
    print(f"⏳ Gerando código para {nome_arquivo}...")
    response = model.generate_content(instrucao)
    
    # Limpeza básica caso o modelo ainda envie as crases do markdown
    codigo = response.text.strip()
    if codigo.startswith("```"):
        codigo = "\n".join(codigo.split("\n")[1:-1])
        
    # Salva diretamente no diretório local
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(codigo)
        
    print(f"✅ Arquivo '{nome_arquivo}' criado com sucesso no diretório local!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso correto: python cli_gemini.py  ")
        sys.exit(1)
        
    arquivo_alvo = sys.argv[1]
    instrucao_usuario = sys.argv[2]
    
    gerar_arquivo(arquivo_alvo, instrucao_usuario)