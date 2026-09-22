from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
for prefix in ['', 'en', 'es']:
    materials=root/prefix/'materiais'
    if not materials.exists(): continue
    with ZipFile(materials/'kit-agent-skills.zip','w',ZIP_DEFLATED) as z:
        for p in sorted((materials/'laboratorio').rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(materials))
        for name in ['briefing.md','rubrica-qa.md','experimentos.csv']:z.write(materials/name,name)
with ZipFile(root/'agent-skills-curso-completo.zip','w',ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if not p.is_file() or set(rel.parts)&{'node_modules','.git','__pycache__','verificacao'} or p.name=='agent-skills-curso-completo.zip':continue
        z.write(p,Path('agent-skills')/rel)
print('Pacotes de laboratório e curso completo gerados.')
