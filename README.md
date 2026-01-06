# twitter bot

bot que busca tweets por uma query específica e retweeta automaticamente usando a API do twitter

o script faz uma busca, retweeta o primeiro tweet disponível e repete o processo a cada 9 horas

---

## features

- busca tweets recentes usando a rota `search/recent`
- filtra por idioma opcional (`--lang`)
- armazena tweets pendentes localmente
- retweeta automaticamente
- log de operações em `paia.log`
- interface visual com `rich`
- agendamento automático via `schedule`

---

## configuração

vá até o dashboard de developer do twitter com a conta do bot

```bash
https://developer.x.com/en/portal/dashboard
```

crie um projeto e um app

<img width="598" height="274" alt="image" src="https://github.com/user-attachments/assets/1fb86081-aa13-476a-989b-f985ae229eb0" />

---

gere as chaves de acesso à API

<img width="601" height="529" alt="image" src="https://github.com/user-attachments/assets/90ab701a-5721-4a2e-88ac-5dd6c4901deb" />

---

edite o arquivo auth.conf com as chaves geradas

<img width="322" height="162" alt="{853FC9BC-86AA-4376-AC94-AF771D04432E}" src="https://github.com/user-attachments/assets/6212da3e-1b2f-425c-9dc3-b61c587078a1" />



---

## instalação

instale as dependências

```bash
pip install -r requirements.txt
```

## rodando

```bash
python bot.py --query [sua-query] --lang [idioma]
```
<div align="center">
  <img src="https://i.imgur.com/jW17SdH.gif"/>
</div>

