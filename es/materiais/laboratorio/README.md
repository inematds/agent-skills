# Laboratorio Agent Skills

Datos sintéticos; no contiene credenciales, llamadas a API ni integración externa.
Requiere Python 3.10+ para ejecutar los scripts. El Codex es necesario solo para probar descubrimiento, disparador y ejecución guiada por la skill.

1. Extraiga el ZIP manteniendo las carpetas ocultas (`.agents/`).
2. Abra la carpeta `laboratorio` en la terminal o en el Codex.
3. Ejecute:

```bash
python3 scripts/gerar_relatorio.py dados/vendas.csv --outdir saidas/rodada-01
python3 scripts/testar_relatorio.py
```

4. Abra los tres archivos de la salida y verifique el total manualmente: R$ 500,00. Loja = 320,00; Site = 180,00; período observado = 2026-09-14 a 2026-09-17.
5. En el Codex, pida: “Use $relatorio-semanal con dados/vendas.csv y guarde en saidas/rodada-02. Muestre la ruta de la skill y las evidencias.”
6. Pruebe también el pedido implícito “Haga un informe semanal de este CSV de ventas” y el negativo “Escriba un anuncio de ventas”. Registre el comportamiento observado.

El generador rechaza CSV vacío, fechas inválidas, negativos, canales vacíos y valores fuera del formato. Estas son reglas didácticas, no una regla contable universal. No deduplica ventas ni aplica un filtro de semana. Una carpeta de salida nueva preserva rondas anteriores.

El QA generado contiene verificaciones internas, no prueba independencia. La suite usa un caso pequeño de una plantilla conocida y casos inválidos. No prueba que el Codex haya activado la skill; esta etapa necesita observarse en su sesión.

Proyecto final: adapte una regla (por ejemplo, límite de valor), documente, agregue un caso y ejecute nuevamente la suite. Guarde la entrada, salida, versión y evidencias.
