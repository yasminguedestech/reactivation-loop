# 🔄 Reactivation Loop — Reengajamento de Motoristas via Canal Externo

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualização-4c72b0?style=flat)
![Produto](https://img.shields.io/badge/Área-Ride%20Hailing-FF6600?style=flat)
![Status](https://img.shields.io/badge/Status-Concluído-38bdf8?style=flat)

> Análise de produto para reativar motoristas inativos da 99 via WhatsApp, identificando a janela ideal de intervenção e o segmento com maior taxa de retorno.

---

## 📌 Contexto do Negócio

Motoristas da 99 ficam inativos após 30 dias sem corridas, impactando diretamente a **disponibilidade de oferta** e a **receita da operação**. A área de Ride Hailing buscou uma solução fora do aplicativo para reengajar esses motoristas antes que o churn se consolidasse.

**Solução proposta:** fluxo automático de reengajamento via WhatsApp ativado a partir dos 15 dias de inatividade, com mensagem personalizada por perfil de motorista.

---

## 🎯 Hipótese

> Motoristas contactados via canal externo nos primeiros 15 dias de inatividade reativam mais do que os não contactados.

---

## 👤 Usuário-alvo

Motoristas com 15 a 45 dias sem corridas, segmentados por tempo de plataforma:

| Perfil | Tempo na plataforma |
|--------|-------------------|
| 🟢 Novo | 0–3 meses |
| 🟡 Recorrente | 3–12 meses |
| 🔵 Veterano | +12 meses |

---

## 📊 Métricas de Sucesso

| Métrica | Critério |
|--------|---------|
| Taxa de reativação (grupo contactado) | ≥ 30% |
| Janela ideal de intervenção | Identificada |
| Segmento com melhor resposta | Identificado para priorização |

---

## 🔬 Metodologia

Simulação com **500 motoristas** (split 50/50 entre grupo contactado e controle), modelando a probabilidade de reativação com base em:

- Recebeu contato externo → **+20pp**
- Perfil Veterano → **+10pp** | Recorrente → **+5pp**
- Inativo há ≤ 20 dias → **+10pp**

---

## 📈 Análise e Resultados

### Gráfico 1 — Contactado vs. Não Contactado

![Contactado vs Controle](graf1_contactado_vs_controle.png)

Motoristas que receberam contato externo apresentaram taxa de reativação **~20 pontos percentuais acima** do grupo controle — superando o critério de sucesso de 30%.

---

### Gráfico 2 — Reativação por Perfil de Motorista

![Reativação por Perfil](graf2_reativacao_por_perfil.png)

**Veteranos** respondem melhor ao contato em todos os perfis, com a maior diferença entre grupo contactado e controle. Novos motoristas apresentam a menor taxa de retorno mesmo com contato.

---

### Gráfico 3 — Janela Ideal de Intervenção

![Janela de Intervenção](graf3_janela_intervencao.png)

A janela **7–20 dias** de inatividade é a mais eficaz. A taxa de reativação cai progressivamente quanto mais tarde acontece o contato — intervir cedo é decisivo.

---

## 💡 Principais Insights

- Contato externo eleva a taxa de reativação em **~20pp** vs. ausência de contato
- A janela de **7–20 dias** de inatividade é a mais eficaz para intervenção
- Motoristas **Veteranos** têm a maior taxa de retorno ao serem contactados
- Intervir após **30 dias** de inatividade reduz significativamente a efetividade

---

## ✅ Recomendação Final

### O que os dados mostram
Motoristas contactados via canal externo reativam significativamente mais do que os não contactados. A janela mais eficaz de intervenção é entre **7 e 20 dias de inatividade**. Motoristas veteranos respondem melhor ao contato do que novos.

### Recomendação
Priorizar o contato externo via WhatsApp nos **primeiros 15 dias de inatividade**, com mensagem personalizada por perfil. Começar pelo segmento **Veterano**, que tem maior taxa de retorno e maior valor histórico para a plataforma.

### Próximos passos
- [ ] Validar hipótese com dados reais de uma coorte pequena
- [ ] Testar duas versões de mensagem (A/B) para otimizar conversão
- [ ] Definir SLA de resposta do motorista para considerar reativação

---

## 🚀 Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/yasminguedestech/reactivation-loop.git
cd reactivation-loop

# 2. Instale as dependências
pip install pandas numpy matplotlib seaborn

# 3. Execute o notebook
jupyter notebook reactivation_loop.ipynb
```

---

## 🗂️ Estrutura do Projeto

```
reactivation-loop/
├── reactivation_loop.ipynb            # Análise completa com visualizações
├── graf1_contactado_vs_controle.png   # Taxa de reativação: contactado vs. controle
├── graf2_reativacao_por_perfil.png    # Reativação por perfil de motorista
├── graf3_janela_intervencao.png       # Janela ideal de intervenção
└── README.md
```

---

## 🛠️ Ferramentas Utilizadas

| Categoria | Ferramenta | Uso |
|-----------|-----------|-----|
| Linguagem | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Desenvolvimento completo |
| Dados | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Manipulação e análise |
| Numérico | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) | Simulação e cálculos |
| Visualização | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat) | Gráficos base |
| Visualização | ![Seaborn](https://img.shields.io/badge/Seaborn-4c72b0?style=flat) | Gráficos estatísticos |
| Notebook | ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white) | Análise interativa |
| Versionamento | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) | Controle de versão |
| Repositório | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) | Hospedagem do projeto |

---

## 📎 Sobre o Projeto

Projeto desenvolvido para portfólio de produto e análise de dados, simulando um cenário real de operações de Ride Hailing. Abrange desde a definição do problema e hipótese de produto até a análise quantitativa com recomendação estratégica orientada a negócio.
