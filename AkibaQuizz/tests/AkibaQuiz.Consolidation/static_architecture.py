from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
app = root / 'AkibaQuiz.Application'
infra = root / 'AkibaQuiz.Infrastructure'
api = root / 'AkibaQuiz.Api'
issues = []
for layer in [app, infra]:
    for path in layer.rglob('*.cs'):
        if any(p in ('bin','obj') for p in path.parts): continue
        content = path.read_text(encoding='utf-8-sig')
        for forbidden in ('GameDto', 'QcmDto', 'QuestionDto', 'RoundDto', 'GameFullDto',
                          'Microsoft.AspNetCore.Mvc', 'HttpContext'):
            if re.search(r'\b'+forbidden+r'\b', content):
                issues.append(f'{path.relative_to(root)} contient {forbidden}')
for name in ('GamesController','QcmController','QuestionsAnswersController', 'ReferencesController'):
    declarations=[]
    for p in (api/'Controllers').glob('*.cs'):
        if re.search(r'\bclass\s+'+name+r'\b',p.read_text(encoding='utf-8-sig')):
            declarations.append(p.name)
    if len(declarations)!=1:
        issues.append(f'{name} defini {len(declarations)} fois : {declarations}')
for i in issues: print('FAIL:',i)
if issues: raise SystemExit(1)
print('PASS: interfaces et dependances des couches + controleurs uniques')
