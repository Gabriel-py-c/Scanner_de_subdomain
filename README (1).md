# 🔍 Subdomain Scanner em Python

Este projeto é um **scanner de subdomínios** escrito em Python.  
Ele utiliza consultas **DNS** e **resolução de IPs** para identificar subdomínios válidos de um domínio alvo, a partir de uma wordlist personalizada.  
Os resultados encontrados são exibidos no terminal e também salvos em um arquivo `Resultado.json`.

---

## 🚀 Funcionalidades
- Descobre subdomínios válidos de um domínio alvo.
- Resolve **endereços IP** separando:
  - **IPv4**
  - **IPv6**
- Verifica registros **CNAME** (aliases de subdomínios).
- Executa consultas em **paralelo (multithread)** para maior velocidade.
- Exporta os resultados em **JSON**.

---

## 📦 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
pip install -r requirements.txt
```

---

## ⚙️ Uso

Execute o script passando dois argumentos:  
1. O domínio alvo  
2. O arquivo de wordlist com possíveis subdomínios  

```bash
python3 scanner.py dominio.com Filtro_wordlist.txt
```

Exemplo prático:
```bash
python3 scanner.py facebook.com wordlists/Filtro_wordlist.txt
```

---

## 📖 Funcionamento

1. O script lê a wordlist de subdomínios.  
2. Para cada item, monta o subdomínio completo (ex: `mail.facebook.com`).  
3. Tenta resolver para IPv4, IPv6 e verificar registro CNAME.  
4. Resultados válidos são exibidos no terminal e salvos em `Resultado.json`.  

---

## 📝 Exemplo de saída

### Terminal:
```
mail.facebook.com - IPv4: ['157.240.20.35'] - IPv6: [] - CNAME: None
static.facebook.com - IPv4: ['31.13.69.16'] - IPv6: [] - CNAME: star-mini.c10r.facebook.com.
ipv6.testfacebook.com - IPv4: [] - IPv6: ['2a03:2880:f10d:83:face:b00c:0:25de'] - CNAME: None
```

### Arquivo `Resultado.json`:
```json
[
    {
        "subdomain": "mail.facebook.com",
        "ipv4": ["157.240.20.35"],
        "ipv6": [],
        "cname": null
    },
    {
        "subdomain": "static.facebook.com",
        "ipv4": ["31.13.69.16"],
        "ipv6": [],
        "cname": "star-mini.c10r.facebook.com."
    },
    {
        "subdomain": "ipv6.testfacebook.com",
        "ipv4": [],
        "ipv6": ["2a03:2880:f10d:83:face:b00c:0:25de"],
        "cname": null
    }
]
```

---

## 📂 Estrutura de pastas (sugerida)

```
meu-projeto/
│── scanner.py           # código principal
│── wordlists/           # wordlist(s) de subdomínios
│   └── Filtro_wordlist.txt    
│── README.md            # este arquivo
```

---

## 📚 Dependências

- Python 3
- [dnspython](https://www.dnspython.org/)  
- Módulos padrão do Python (`socket`, `json`, `concurrent.futures`)

Instale manualmente com:
```bash
pip install dnspython
```

Ou via `requirements.txt`:
```
dnspython
```

---

## ⚠️ Aviso legal
Este projeto é destinado **exclusivamente para fins educacionais e de segurança defensiva**.  
Não utilize contra sistemas sem autorização explícita do responsável. O uso indevido é de total responsabilidade do usuário.
