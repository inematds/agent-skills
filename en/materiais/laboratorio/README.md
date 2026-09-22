# Agent Skills Lab

Synthetic data; it contains no credentials, API calls, or external integrations.
Requires Python 3.10+ to run the scripts. Codex is only needed to test discovery, trigger, and skill-guided execution.

1. Extract the ZIP while keeping hidden folders (`.agents/`).
2. Open the folder `laboratorio` in the terminal or in Codex.
3. Run:

```bash
python3 scripts/gerar_relatorio.py dados/vendas.csv --outdir saidas/rodada-01
python3 scripts/testar_relatorio.py
```

4. Open the three output files and check the total manually: R$ 500,00. Loja = 320,00; Site = 180,00; observed period = 2026-09-14 to 2026-09-17.
5. In Codex, ask: “Use $relatorio-semanal with dados/vendas.csv and save it in saidas/rodada-02. Show the skill path and the evidence.”
6. Also test the implied request “Make a weekly report from this sales CSV” and the negative “Write a sales ad.” Record the observed behavior.

The generator rejects empty CSV, invalid dates, negatives, empty channels, and values outside the expected format. These are teaching rules, not a universal accounting rule. It doesn’t deduplicate sales or apply a week filter. A new output folder preserves earlier runs.

The generated QA includes internal checks; it doesn’t prove independent verification. The suite uses a small known-answer case and invalid cases. It doesn’t prove that Codex triggered the skill; that step must be observed in your session.

Final project: adapt a rule (for example, a value limit), document it, add a case, and run the suite again. Save the input, output, version, and evidence.
