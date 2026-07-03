# 🤖 GCM-BOT - GUIA RÁPIDO PARA MOBILE

## ⚡ RESUMO (Leia primeiro!)

Seu bot precisa estar rodando em um **computador** ou **servidor** 24/7. O celular serve apenas para **usar** os comandos no Discord.

---

## 📱 O que fazer AGORA (Celular)

### 1️⃣ Abra o Discord no celular

### 2️⃣ Vá para seu servidor

### 3️⃣ Procure o bot "GCM-BOT" na lista de membros
- Se estiver com **ponto verde** = bot está online ✅
- Se não aparecer = bot precisa ser adicionado

---

## 💻 O que você PRECISA fazer (Computador)

O bot **PRECISA rodar em um computador** para funcionar.

### Passo 1: Clone o repositório
```bash
git clone https://github.com/luixrp2006-cmyk/GCM-BOT.git
cd GCM-BOT
```

### Passo 2: Execute o setup automático
```bash
python auto_setup.py
```

**O script vai:**
1. ✅ Instalar tudo automaticamente
2. ✅ Pedir seu token do Discord
3. ✅ Gerar link para adicionar ao servidor
4. ✅ Iniciar o bot

### Passo 3: Mantenha rodando
- O bot precisa ficar **rodando continuamente**
- Deixe o computador ligado
- Ou use um **servidor na nuvem** (Heroku, AWS, etc)

---

## 🔑 Como obter seu Token (Computador)

1. Acesse: https://discord.com/developers/applications
2. Clique em "New Application"
3. Nome: **GCM-BOT**
4. Vá para "Bot" → "Add Bot"
5. Clique em **Copy** (botão com token)
6. Cole quando o script pedir

---

## 📖 Usando os Comandos (Mobile)

Agora que o bot está online, você pode usar no Discord:

### Bater Ponto
```
/ponto_entrada      (Registra entrada)
/ponto_saida        (Registra saída)
/meu_ponto          (Vê seu ponto)
```

### Viaturas
```
/pegar_viatura placa:"ABC-1234"
/devolver_viatura placa:"ABC-1234"
/listar_viaturas
```

### Ocorrências
```
/criar_ocorrencia titulo:"..." descricao:"..." local:"..."
/ver_ocorrencia id_ocorrencia:"OC-..."
/fechar_ocorrencia id_ocorrencia:"OC-..."
```

---

## ❓ Perguntas Frequentes

### P: O bot desapareceu do Discord
**R:** Significa que o computador desligou ou o programa parou. Execute novamente:
```bash
python main.py
```

### P: Não vejo os comandos no Discord
**R:** 
1. Aguarde 1 minuto após iniciar o bot
2. Feche e abra o Discord novamente (puxe para baixo)
3. Digite "/" para atualizar

### P: Como fazer o bot ficar online 24/7?
**R:** Use um **servidor na nuvem** gratuito:
- Replit.com
- Heroku (agora pago)
- Railway.app
- Render.com

---

## 🚀 Próximos Passos

1. **No computador:** Execute `python auto_setup.py`
2. **Cole seu token** quando pedido
3. **Deixe rodando** enquanto quiser usar
4. **No celular:** Teste os comandos no Discord

---

## 📞 Precisa de ajuda?

- GitHub: https://github.com/luixrp2006-cmyk/GCM-BOT
- Abra uma Issue com sua dúvida

---

**Você consegue! 💪**
