# Reactivation Loop — Reengajamento de Motoristas via Canal Externo

Análise de produto para reativar motoristas inativos da 99 via WhatsApp, identificando a janela ideal de intervenção e o segmento com maior taxa de retorno.

---

## Contexto

Motoristas ficam inativos após 30 dias sem corridas, impactando a disponibilidade de oferta na plataforma. A área de Ride Hailing buscou uma solução fora do app para engajá-los antes que o churn se consolidasse.

**Solução proposta:** fluxo automático de reengajamento via WhatsApp ativado a partir dos 15 dias de inatividade, com mensagem personalizada por perfil de motorista.

---

## Hipótese

> Motoristas contactados via canal externo nos primeiros 15 dias de inatividade reativam mais do que os não contactados.

---

## Usuário-alvo

Motoristas com 15 a 45 dias sem corridas, segmentados por tempo de plataforma:

| Perfil | Tempo na plataforma |
|--------|-------------------|
| Novo | 0–3 meses |
| Recorrente | 3–12 meses |
| Veterano | +12 meses |

---

## Metodologia

Simulação com 500 motoristas (split 50/50 entre grupo contactado e controle), modelando a probabilidade de reativação com base em:
- Recebeu contato externo (+20pp)
- Perfil Veterano (+10pp) ou Recorrente (+5pp)
- Inativo há ≤ 20 dias (+10pp)

---

## Resultados

### Taxa de reativação: contactado vs. controle
Motoristas que receberam contato externo apresentaram taxa de reativação ~20 pontos percentuais acima do grupo controle, superando o critério de sucesso de 30%.

### Melhor janela de intervenção
A janela **7–20 dias** concentrou a maior taxa de reativação entre os motoristas contactados — intervir cedo é mais eficaz.

### Segmento prioritário
**Veteranos** responderam melhor ao contato do que Recorrentes e Novos, combinando maior taxa de retorno com maior valor histórico para a plataforma.

![Gráficos de análise](reactivation_loop.png)

---

## Recomendação

Priorizar contato via WhatsApp nos **primeiros 15 dias de inatividade**, começando pelo segmento **Veterano**.

### Próximos passos
- Validar com dados reais em coorte pequena
- Teste A/B com duas versões de mensagem
- Definir SLA de resposta para considerar reativação confirmada

---

## Estrutura do repositório

```
reactivation-loop/
├── reactivation_loop.ipynb   # Análise completa com visualizações
├── reactivation_loop.png     # Output dos gráficos (gerado pelo notebook)
└── README.md
```

---

## Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn`
