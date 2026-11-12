"""staging/<id>.html + <id>.json 을 index.html 에 합친다. 순서는 ORDER. 다시 돌려도 같은 결과."""
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
# 첫 장·끝 장 '영상으로 보기' 버튼에 쓸 짧은 채널 이름
SHORT = {'그로잉살롱GrowingSalon': '그로잉살롱', '아는원장의 쉬운 커트, 쉬운 미용': '아는원장', '하이예나 Hiyena': '하이예나',
    '페이지원 헤어랩 | 미용사를 위한 성장 채널': '페이지원 헤어랩', 'Training of hairstylists (ARTIST FUN)': 'ARTIST FUN',
    '로아티 Roati': '로아티', '파마대통령 마르 원장': '마르 원장', '미남들 - 미용하는 남자들': '미남들', '훠니 Huoney': '훠니',
    '인천 부천 남자커트 이용학원': '남자커트 이용학원', 'KINGSTON 킹스턴': '킹스턴', '미르쌤 Mir': '미르쌤', '서현SeoHyun': '서현',
    '헤어광장 JMW PROFESSIONAL': '헤어광장', '차홍 CHAHONG': '차홍', '윤원장 (SJbeautyhair)': '윤원장',
    '한컷한컷 임지유(HanCut HanCut Jiyu)': '한컷한컷 임지유', '광국쌤 아름다운작업장': '광국쌤', '황원장의 남자머리': '황원장'}
def videos(srcs):
    # [영상 id, 버튼 이름]. 한 스타일에 같은 채널이 두 번 나오면 뒤에 번호를 붙인다
    names = [SHORT.get(v['channel'], v['channel']) for v in srcs]
    out = []
    for i, (v, nm) in enumerate(zip(srcs, names)):
        if names.count(nm) > 1:
            nm += ' ' + str(names[:i + 1].count(nm))
        out.append([v['id'], nm])
    return out
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
    metas.append({'id': sid, 'name': m['name'], 'group': m.get('group', '남자'), 'chapters': ch, 'videos': videos(m.get('sources', []))})
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
