import json
import sys
import dns.resolver
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================
# Script para descoberta de subdomínios
# - Recebe como entrada:
#   1º argumento: domínio alvo (ex: facebook.com)
#   2º argumento: wordlist com possíveis subdomínios
# - Faz resolução DNS para encontrar:
#   -> IPv4
#   -> IPv6
#   -> CNAME (se existir)
# - Usa threads para acelerar o processo
# - Salva resultados em arquivo JSON
# ============================

# Argumentos da linha de comando
dominio = sys.argv[1]       # Domínio alvo
wordlist_file = sys.argv[2] # Arquivo contendo possíveis subdomínios

# Configuração do resolvedor DNS
resolver = dns.resolver.Resolver()
resolver.timeout = 2    # Tempo máximo de resposta por tentativa
resolver.lifetime = 2   # Tempo máximo de vida para a consulta
tentativas = 2          # Número de tentativas em caso de timeout

# Função que verifica se um subdomínio existe
def verificar_subdomain(d):
    subdomain_completo = f"{d}.{dominio}"  # Exemplo: mail.facebook.com
    tentativa = tentativas

    while tentativa > 0:
        try:
            # --- IPv4 ---
            ipv4 = list(set([
                item[4][0] 
                for item in socket.getaddrinfo(subdomain_completo, None, socket.AF_INET)
            ]))

            # --- IPv6 ---
            ipv6 = []
            try:
                ipv6 = list(set([
                    item[4][0] 
                    for item in socket.getaddrinfo(subdomain_completo, None, socket.AF_INET6)
                ]))
            except socket.gaierror:
                pass  # Se não tiver IPv6, apenas ignora

            # --- CNAME ---
            try:
                resposta = resolver.resolve(subdomain_completo, "CNAME")
                cname = str(resposta[0].target)
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                cname = None

            # Se encontrou qualquer IP, retorna as informações
            if ipv4 or ipv6:
                return {
                    "subdomain": subdomain_completo,
                    "ipv4": ipv4,
                    "ipv6": ipv6,
                    "cname": cname
                }
            else:
                return None

        # Erros comuns: subdomínio não existe ou não responde
        except (socket.gaierror, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            return None

        # Timeout -> tenta de novo até esgotar tentativas
        except dns.resolver.Timeout:
            tentativa -= 1

    return None


# --- Lê a wordlist com os possíveis subdomínios ---
with open(wordlist_file) as f:
    subdominios = [d.strip() for d in f.readlines()]

# Lista para armazenar os resultados encontrados
resultados = []

# --- Executa em paralelo usando ThreadPoolExecutor ---
with ThreadPoolExecutor(max_workers=20) as executor:
    # Cria tarefas para cada subdomínio
    futures = {executor.submit(verificar_subdomain, d): d for d in subdominios}

    # Processa os resultados conforme forem concluídos
    for future in as_completed(futures):
        resultado = future.result()
        if resultado:
            # Mostra no terminal
            print(f"{resultado['subdomain']} - IPv4: {resultado['ipv4']} - IPv6: {resultado['ipv6']} - CNAME: {resultado['cname']}")
            # Armazena no array final
            resultados.append(resultado)

# --- Salva os resultados em arquivo JSON ---
with open("Resultado.json", "w") as f:
    json.dump(resultados, f, indent=4)
