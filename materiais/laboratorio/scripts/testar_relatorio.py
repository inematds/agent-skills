#!/usr/bin/env python3
import json,tempfile,unittest
from pathlib import Path
from gerar_relatorio import gerar,calcular
class Contrato(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def entrada(self,text):p=self.root/'entrada.csv';p.write_text(text,encoding='utf-8');return p
    def test_gabarito_independente(self):
        p=Path(__file__).resolve().parents[1]/'dados/vendas.csv';d=gerar(p,self.root/'saida')
        self.assertEqual(d['total'],'500.00');self.assertEqual(d['registros'],4)
        self.assertEqual(d['canais'],{'Loja':'320.00','Site':'180.00'})
        self.assertEqual((d['periodo_inicio'],d['periodo_fim']),('2026-09-14','2026-09-17'))
        text=(self.root/'saida/relatorio.md').read_text();self.assertIn('R$ 500,00',text);self.assertIn('2026-09-14 a 2026-09-17',text)
    def invalid(self,text,pattern):
        with self.assertRaisesRegex(ValueError,pattern):gerar(self.entrada(text),self.root/'saida')
        self.assertFalse((self.root/'saida').exists())
    def test_coluna_ausente(self):self.invalid('data,canal\n2026-09-14,Loja\n','Colunas')
    def test_vazio(self):self.invalid('data,canal,valor\n','sem registros')
    def test_data_invalida(self):self.invalid('data,canal,valor\n2026-02-30,Loja,10.00\n','data inválida')
    def test_virgula_decimal(self):self.invalid('data,canal,valor\n2026-09-14,Loja,"10,00"\n','duas casas')
    def test_negativo(self):self.invalid('data,canal,valor\n2026-09-14,Loja,-10.00\n','não negativo')
    def test_nan(self):self.invalid('data,canal,valor\n2026-09-14,Loja,NaN\n','duas casas')
    def test_canal_vazio(self):self.invalid('data,canal,valor\n2026-09-14,,10.00\n','canal vazio')
    def test_casas_extras(self):self.invalid('data,canal,valor\n2026-09-14,Loja,10.001\n','duas casas')
    def test_campo_extra(self):self.invalid('data,canal,valor\n2026-09-14,Loja,10.00,extra\n','quantidade')
    def test_duplicacao_cabecalho(self):self.invalid('data,canal,valor,valor\n2026-09-14,Loja,10.00,10.00\n','duplicadas')
    def test_preserva_saida_anterior(self):
        p=self.entrada('data,canal,valor\n2026-09-14,Loja,10.00\n');out=self.root/'saida';gerar(p,out)
        before=(out/'relatorio.md').read_bytes()
        with self.assertRaisesRegex(ValueError,'já contém'):gerar(p,out)
        self.assertEqual(before,(out/'relatorio.md').read_bytes())
    def test_entrada_preservada_e_ordem_datas(self):
        p=self.entrada('data,canal,valor\n2026-09-17,Loja,0.10\n2026-09-14,Loja,0.20\n');before=p.read_bytes();d=gerar(p,self.root/'saida')
        self.assertEqual(d['total'],'0.30');self.assertEqual(d['periodo_inicio'],'2026-09-14');self.assertEqual(before,p.read_bytes())
if __name__=='__main__':unittest.main(verbosity=2)
