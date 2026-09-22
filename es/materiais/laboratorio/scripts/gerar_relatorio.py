#!/usr/bin/env python3
"""Laboratório educativo: contrato explícito, cálculos locais, sem API."""
import argparse,csv,json,re,sys
from pathlib import Path
from datetime import date
from decimal import Decimal

def calcular(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or not {'data','canal','valor'}.issubset(reader.fieldnames):
            raise ValueError('Colunas obrigatórias: data, canal, valor.')
        if len(reader.fieldnames)!=len(set(reader.fieldnames)):
            raise ValueError('Cabeçalho contém colunas duplicadas.')
        datas=[];canais={};total=Decimal('0.00')
        for n,row in enumerate(reader,2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'Linha {n}: quantidade de campos inválida.')
            d=row['data'].strip();c=row['canal'].strip();v=row['valor'].strip()
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',d):raise ValueError(f'Linha {n}: use data AAAA-MM-DD.')
            try: dt=date.fromisoformat(d)
            except ValueError:raise ValueError(f'Linha {n}: data inválida.') from None
            if not c or len(c)>80 or any(ch in c for ch in '\r\n|'):
                raise ValueError(f'Linha {n}: canal vazio, longo ou com caracteres não permitidos.')
            if not re.fullmatch(r'\d{1,12}\.\d{2}',v):
                raise ValueError(f'Linha {n}: valor deve ser não negativo, com ponto e duas casas; até 12 dígitos inteiros.')
            value=Decimal(v);datas.append(dt);total+=value;canais[c]=canais.get(c,Decimal('0.00'))+value
        if not datas:raise ValueError('Arquivo sem registros de vendas.')
    return {'periodo_inicio':min(datas).isoformat(),'periodo_fim':max(datas).isoformat(),'registros':len(datas),'moeda':'BRL','total':str(total),'canais':{k:str(v) for k,v in sorted(canais.items())}}

def br(value):return f'{Decimal(value):,.2f}'.replace(',','X').replace('.',',').replace('X','.')
def texto_seguro(s):
    for ch in ('\\','`','*','_','[',']','<','>','#'):
        s=s.replace(ch,'\\'+ch)
    return s

def gerar(path,outdir):
    data=calcular(path) # validar tudo antes de criar qualquer saída
    out=Path(outdir)
    if out.resolve()==Path(path).resolve():raise ValueError('Saída deve ser uma pasta diferente da entrada.')
    if out.exists() and any((out/name).exists() for name in ['relatorio.md','dados-calculados.json','qa.json']):
        raise ValueError('A pasta já contém resultados. Use outra pasta para preservar a execução anterior.')
    out.mkdir(parents=True,exist_ok=True)
    lines=['# Relatório semanal','',f'Período observado: {data["periodo_inicio"]} a {data["periodo_fim"]}',f'Moeda: {data["moeda"]}',f'Registros: {data["registros"]}',f'Total: R$ {br(data["total"])}','','## Totais por canal','','| Canal | Total |','| --- | ---: |']
    lines += [f'| {texto_seguro(k)} | R$ {br(v)} |' for k,v in data['canais'].items()]
    lines += ['','## Pendências','','Nenhuma inconsistência detectada pelas regras deste laboratório.','O período é observado no arquivo; não foi aplicado filtro de semana.','Não houve conciliação com sistemas externos nem análise de causas.','']
    (out/'relatorio.md').write_text('\n'.join(lines),encoding='utf-8')
    (out/'dados-calculados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Checagens internas, NÃO uma auditoria independente: declarar escopo.
    soma_canais=sum((Decimal(v) for v in data['canais'].values()),Decimal('0.00'))
    qa={'entrada':str(path),'metodo':'Checagens internas do gerador; conferir o caso de referência com testar_relatorio.py.','checks':[{'criterio':'canais reconciliam com total','passou':soma_canais==Decimal(data['total']),'obtido':str(soma_canais)},{'criterio':'período e registros presentes','passou':bool(datas_presentes(data))}],'limites':['Não confirma completude da fonte.','Não comprova acionamento da skill pelo Codex.','Não realiza revisão editorial por agente.']}
    (out/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data

def datas_presentes(data):return data['periodo_inicio'] and data['periodo_fim'] and data['registros']>0

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv');p.add_argument('--outdir',required=True);a=p.parse_args()
    try:gerar(a.csv,a.outdir)
    except (ValueError,OSError,csv.Error) as exc:print(f'Erro: {exc}',file=sys.stderr);return 1
    print(f'Relatório, dados e QA salvos em {a.outdir}');return 0
if __name__=='__main__':raise SystemExit(main())
