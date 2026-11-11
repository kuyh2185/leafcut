"""staging/<id>.html + <id>.json 을 index.html 에 합친다. 순서는 ORDER. 다시 돌려도 같은 결과."""
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
ORDER = ['gail', 'drop', 'ase', 'dandy', 'crop', 'ivy', 'regent', 'pomade', 'shadow', 'hush', 'bob', 'longlayer', 'tassel', 'hime', 'seethru', 'hippie', 'build', 'wave', 'magic']
idx = root / 'index.html'
s = idx.read_text(encoding='utf-8')
html, metas = [], []
for sid in ORDER:
    h, j = root / 'staging' / f'{sid}.html', root / 'staging' / f'{sid}.json'
    if not (h.exists() and j.exists()):
        sys.exit(f'staging/{sid}.html·json 이 없음: 합치면 이 스타일이 사라지니 중단. ORDER에서 빼거나 staging을 채운 뒤 다시 실행')
    m = json.loads(j.read_text(encoding='utf-8'))
    frag = h.read_text(encoding='utf-8').strip()
    html.append(f'<!-- {m["name"]} -->\n' + frag)
    ch = [{k: v for k, v in c.items() if k in ('id', 'name', 'seq')} for c in m['chapters']]
    metas.append({'id': sid, 'name': m['name'], 'group': m.get('group', '남자'), 'chapters': ch})
    print('add', sid, frag.count('<section'), 'cards')
a, b = s.index('<!-- STYLES:BEGIN -->'), s.index('<!-- STYLES:END -->')
s = s[:a] + '<!-- STYLES:BEGIN -->\n' + '\n\n'.join(html) + '\n' + s[b:]
js = ''.join(',\n    ' + json.dumps(m, ensure_ascii=False) for m in metas)
a = s.index('/*STYLES*/') if '/*STYLES*/' in s else None
# 표식 사이를 통째로 바꾼다
start = s.index("{id:'leaf'")
end = s.index('/*STYLES*/')
leaf_end = s.index(']}', start) + 2
s = s[:leaf_end] + js + '\n    ' + s[end:]
idx.write_text(s, encoding='utf-8')
