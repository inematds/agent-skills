# Laboratório Agent Skills

Dados sintéticos; não contém credenciais, chamadas de API ou integração externa.
Requer Python 3.10+ para executar os scripts. O Codex é necessário apenas para testar descoberta, gatilho e execução orientada pela skill.

1. Extraia o ZIP mantendo as pastas ocultas (`.agents/`).
2. Abra a pasta `laboratorio` no terminal ou no Codex.
3. Execute:

```bash
python3 scripts/gerar_relatorio.py dados/vendas.csv --outdir saidas/rodada-01
python3 scripts/testar_relatorio.py
```

4. Abra os três arquivos da saída e confira o total manualmente: R$ 500,00. Loja = 320,00; Site = 180,00; período observado = 2026-09-14 a 2026-09-17.
5. No Codex, peça: “Use $relatorio-semanal com dados/vendas.csv e salve em saidas/rodada-02. Mostre o caminho da skill e as evidências.”
6. Teste também o pedido implícito “Faça um relatório semanal deste CSV de vendas” e o negativo “Escreva um anúncio de vendas”. Registre o comportamento observado.

O gerador rejeita CSV vazio, datas inválidas, negativos, canais vazios e valores fora do formato. Essas são regras didáticas, não uma regra contábil universal. Não deduplica vendas nem aplica filtro de semana. Uma pasta de saída nova preserva rodadas anteriores.

O QA gerado contém checagens internas, não prova independente. A suíte usa um caso pequeno de gabarito conhecido e casos inválidos. Ela não prova que o Codex acionou a skill; essa etapa precisa ser observada na sua sessão.

Projeto final: adapte uma regra (por exemplo, limite de valor), documente-a, acrescente um caso e execute novamente a suíte. Guarde a entrada, saída, versão e evidências.
