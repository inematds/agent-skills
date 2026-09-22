const fs=require('fs'),ts=require('/home/nmaldaner/projetos/portal/node_modules/typescript');
const file=process.argv[2],src=fs.readFileSync(file,'utf8'),ast=ts.createSourceFile(file,src,ts.ScriptTarget.Latest,true,ts.ScriptKind.JS),out=[];
function walk(n){if(ts.isStringLiteral(n)||ts.isNoSubstitutionTemplateLiteral(n))out.push({value:n.text,start:Array.from(src.slice(0,n.getStart(ast))).length,end:Array.from(src.slice(0,n.end)).length});ts.forEachChild(n,walk)}walk(ast);console.log(JSON.stringify(out));
