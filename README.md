# 🚔 GCM-BOT - Discord Bot para Gestão Operacional

Bot Discord completo para gestão de Guardas Municipais, com funcionalidades de controle de ponto, frota de viaturas e registro de ocorrências.

## 🎯 Funcionalidades

### 📋 **Controle de Ponto**
- `/ponto_entrada` - Registra entrada do guarda
- `/ponto_saida` - Registra saída do guarda
- `/meu_ponto` - Visualiza ponto do dia atual

### 🚗 **Gestão de Viaturas**
- `/adicionar_viatura` - Adiciona nova viatura ao sistema
- `/pegar_viatura` - Atribui viatura ao guarda
- `/devolver_viatura` - Devolve viatura como disponível
- `/listar_viaturas` - Lista todas as viaturas da frota
- `/info_viatura` - Visualiza detalhes de uma viatura

### 🚨 **Registro de Ocorrências**
- `/criar_ocorrencia` - Cria nova ocorrência/incidente
- `/ver_ocorrencia` - Visualiza detalhes de uma ocorrência
- `/atribuir_ocorrencia` - Atribui ocorrência a um guarda
- `/atualizar_ocorrencia` - Adiciona atualização à ocorrência
- `/fechar_ocorrencia` - Marca ocorrência como resolvida
- `/ocorrencias_abertas` - Lista todas as ocorrências abertas

## 🚀 Instalação

### Pré-requisitos
- Python 3.9+
- pip (gerenciador de pacotes Python)
- Uma aplicação Discord Bot configurada

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/luixrp2006-cmyk/GCM-BOT.git
cd GCM-BOT
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```
DISCORD_TOKEN=seu_token_do_bot_aqui
DISCORD_PREFIX=!
DATABASE_URL=sqlite:///gcm_bot.db
```

4. **Obtenha seu token do Discord**
- Vá para [Discord Developer Portal](https://discord.com/developers/applications)
- Crie uma nova aplicação
- Na seção "Bot", clique em "Add Bot"
- Copie o token e cole em `.env`

5. **Configure permissões do bot**
Na seção "OAuth2 > URL Generator":
- Selecione `bot` em Scopes
- Selecione as permissões:
  - `Send Messages`
  - `Embed Links`
  - `Read Message History`
  - `Manage Messages`

6. **Execute o bot**
```bash
python main.py
```

## 💾 Banco de Dados

O bot utiliza **SQLite** por padrão, com suporte a MongoDB.

### Estrutura do Banco

- **timesheet** - Registro de entradas e saídas
- **vehicles** - Dados das viaturas
- **incidents** - Registro de ocorrências
- **incident_updates** - Histórico de atualizações das ocorrências

## 📊 Exemplos de Uso

### Bater Ponto
```
/ponto_entrada          (Registra entrada)
/ponto_saida            (Registra saída)
/meu_ponto              (Visualiza seu ponto)
```

### Registrar Viatura
```
/adicionar_viatura placa:"ABC-1234" modelo:"Fiat Uno Mille"
/pegar_viatura placa:"ABC-1234"
/devolver_viatura placa:"ABC-1234"
```

### Criar Ocorrência
```
/criar_ocorrencia titulo:"Acidente na Avenida Principal" descricao:"Colisão entre 2 veículos" local:"Avenida Principal, 100" prioridade:"alta"
/ver_ocorrencia id_ocorrencia:"OC-20260703-A1B2C3D4"
/fechar_ocorrencia id_ocorrencia:"OC-20260703-A1B2C3D4"
```

## 🔧 Configuração Avançada

### Usar MongoDB em vez de SQLite

1. Instale o driver MongoDB:
```bash
pip install pymongo
```

2. Modifique `src/database.py` para usar MongoDB (veja comentários no arquivo)

3. Configure em `.env`:
```
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/gcm_bot
```

### Canais de Log

Configure um canal para logs automáticos em `.env`:
```
LOG_CHANNEL_ID=seu_id_do_canal
```

## 📝 Estrutura do Projeto

```
GCM-BOT/
├── main.py                 # Entrada principal
├── requirements.txt        # Dependências
├── .env.example           # Variáveis de ambiente
└── src/
    ├── database.py        # Gerenciador de banco de dados
    └── cogs/
        ├── timesheet.py   # Cog de ponto
        ├── vehicles.py    # Cog de viaturas
        └── incidents.py   # Cog de ocorrências
```

## 🔐 Segurança

- ✅ Variáveis sensíveis em `.env` (nunca comitar)
- ✅ Validação de permissões (admin-only para certas ações)
- ✅ Validação de entrada de dados
- ✅ Tratamento de erros abrangente

## 📄 Licença

Este projeto está sob licença MIT.

## 👨‍💼 Suporte

Para reportar bugs ou sugerir funcionalidades, abra uma [Issue](https://github.com/luixrp2006-cmyk/GCM-BOT/issues).

---

**Desenvolvido por:** luixrp2006-cmyk  
**Status:** Em desenvolvimento ativo 🚀
