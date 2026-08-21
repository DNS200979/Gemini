import os
import sys
import subprocess
import google.generativeai as genai

# Configura a API usando a variável de ambiente
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def executar_git(comando):
    """Executa um comando no terminal e retorna se teve sucesso."""
    try:
        # capture_output garante que o erro não suje a tela a menos que dê falha
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {comando}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar '{comando}':")
        print(e.stderr)
        return False

def gerar_e_versionar(nome_arquivo, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    instrucao = f"Escreva o código para a seguinte solicitação: '{prompt}'. Retorne APENAS o código limpo, sem explicações em texto e sem formatação markdown (como ```python)."
    
    print(f"⏳ Gerando código para {nome_arquivo}...")
    response = model.generate_content(instrucao)
    
    # Limpeza básica do código
    codigo = response.text.strip()
    if codigo.startswith("```"):
        codigo = "\n".join(codigo.split("\n")[1:-1])
        
    # Salva o arquivo localmente
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(codigo)
        
    print(f"✅ Arquivo '{nome_arquivo}' salvo localmente!\n")
    
    # === INÍCIO DA AUTOMAÇÃO GIT ===
    print("🚀 Sincronizando com o GitHub...")
    
    # 1. Adiciona o arquivo
    if executar_git(f'git add "{nome_arquivo}"'):
        
        # 2. Faz o commit (usando o nome do arquivo na mensagem)
        mensagem_commit = f"feat: código auto-gerado para {nome_arquivo}"
        if executar_git(f'git commit -m "{mensagem_commit}"'):
            
            # 3. Faz o push para o repositório remoto
            print("⏳ Enviando para o GitHub (push)...")
            executar_git('git push')
            print("🎉 Fluxo completo finalizado!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso correto: python cli_gemini.py <nome_do_arquivo> <sua_instrução>")
        sys.exit(1)
        
    arquivo_alvo = sys.argv[1]
    instrucao_usuario = sys.argv[2]
    
    gerar_e_versionar(arquivo_alvo, instrucao_usuario)
