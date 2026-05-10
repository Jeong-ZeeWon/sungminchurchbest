#!/usr/bin/env python3
"""
성민교회 '한 주간 예배 담당자' 자동 업데이트
Notion 페이지에서 데이터를 읽어 worship.html을 재생성합니다.
"""
import os, re, sys, requests
from datetime import datetime

NOTION_TOKEN = os.environ.get('NOTION_TOKEN', '')
PAGE_ID = '35b5e604d8c680aea0c4d47fc08c83f7'
OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'worship.html')

DAYS_KR = ['월', '화', '수', '목', '금', '토']
DAY_IDX = {d: i for i, d in enumerate(DAYS_KR)}
YEAR    = datetime.now().year


def notion_get(path):
    r = requests.get(
        f'https://api.notion.com/v1/{path}',
        headers={
            'Authorization': f'Bearer {NOTION_TOKEN}',
            'Notion-Version': '2022-06-28',
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def fetch_lines():
    data = notion_get(f'blocks/{PAGE_ID}/children')
    lines = []
    for block in data.get('results', []):
        bt = block.get('type', '')
        if bt in ('paragraph', 'heading_1', 'heading_2', 'heading_3',
                  'bulleted_list_item', 'numbered_list_item'):
            text = ''.join(t.get('plain_text', '') for t in block[bt].get('rich_text', []))
            if text.strip():
                lines.append(text.strip())
        elif bt == 'divider':
            lines.append('---')
    return lines


def expand_days(s):
    s = s.strip()
    if '-' in s:
        a, b = s.split('-', 1)
        a, b = a.strip(), b.strip()
        if a in DAY_IDX and b in DAY_IDX:
            return list(range(DAY_IDX[a], DAY_IDX[b] + 1))
    return [DAY_IDX[d.strip()] for d in s.split(',') if d.strip() in DAY_IDX]


def parse_dawn_row(line):
    if ':' not in line:
        return None, [''] * 6
    role, rest = line.split(':', 1)
    persons = [''] * 6
    for m in re.finditer(r'([^,()]+?)\(([^)]+)\)', rest):
        name = m.group(1).strip()
        for idx in expand_days(m.group(2)):
            if 0 <= idx < 6:
                persons[idx] = name
    return role.strip(), persons


def parse_sections(lines):
    sections, cur = [], []
    for line in lines:
        if line == '---':
            if cur:
                sections.append(cur)
            cur = []
        elif line:
            cur.append(line)
    if cur:
        sections.append(cur)
    return sections


def parse_all(lines):
    dawn, wednesday, friday = {}, {}, {}
    for section in parse_sections(lines):
        if not section:
            continue
        title = section[0]

        if '새벽기도회' in title:
            m = re.search(r'(\d+)/(\d+)[^\d]+(\d+)', title)
            dawn['month']     = m.group(1) if m else '?'
            dawn['start_day'] = m.group(2) if m else '?'
            dawn['end_day']   = m.group(3) if m else '?'
            dawn['roles'] = {}
            for line in section[1:]:
                role, persons = parse_dawn_row(line)
                if role:
                    dawn['roles'][role] = persons

        elif '수요예배' in title:
            m = re.search(r'(\d+)/(\d+)', title)
            wednesday['month'] = m.group(1) if m else '?'
            wednesday['day']   = m.group(2) if m else '?'
            wednesday['roles'] = {}
            for line in section[1:]:
                if ':' in line:
                    r, v = line.split(':', 1)
                    wednesday['roles'][r.strip()] = v.strip()

        elif '금요성령집회' in title:
            m = re.search(r'(\d+)/(\d+)', title)
            friday['month'] = m.group(1) if m else '?'
            friday['day']   = m.group(2) if m else '?'
            friday['roles'], friday['prayer_warriors'] = {}, []
            for line in section[1:]:
                if ':' in line:
                    r, v = line.split(':', 1)
                    r, v = r.strip(), v.strip()
                    if r == '기도용사':
                        friday['prayer_warriors'] = v.split()
                    else:
                        friday['roles'][r] = v

    return dawn, wednesday, friday


def clean_name(name):
    if not name:
        return '-'
    name = name.strip()
    if name.endswith('목사님'):
        return '목사님'
    return re.sub(r'\s*목사\s*$', '', name).strip() or name


def chip_html(name, role):
    name = clean_name(name)
    if name == '목사님':
        css = 'chip-pastor'
    elif role == '설교':
        css = 'chip-sermon'
    elif role == '자막':
        css = 'chip-sub'
    else:
        css = 'chip-plain'
    return f'<span class="chip {css}">{name}</span>'


CSS = """
    :root {
      --bg:        #F0EDE6;
      --white:     #FFFFFF;
      --text:      #3A2E26;
      --soft:      #9E8E80;
      --border:    #E6DDD4;
      --green:     #77C17E;
      --green-bg:  #EAF6EB;
      --pink:      #F2889A;
      --pink-bg:   #FDEDF0;
      --yellow:    #F5C842;
      --yellow-bg: #FFFAED;
      --blue:      #72B6E0;
      --blue-bg:   #EAF4FC;
      --purple:    #9B8EC4;
      --purple-bg: #F0EDFA;
      --orange:    #F09050;
      --orange-bg: #FEF3EC;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg);
      background-image:
        radial-gradient(ellipse at 10% 15%, rgba(119,193,126,.18) 0%, transparent 45%),
        radial-gradient(ellipse at 90% 85%, rgba(242,136,154,.14) 0%, transparent 45%),
        radial-gradient(ellipse at 60% 40%, rgba(245,200,66,.10) 0%, transparent 40%);
      font-family: 'Noto Sans KR', sans-serif;
      color: var(--text);
      min-height: 100vh;
      padding: 28px 14px 56px;
    }
    .wrap { max-width: 600px; margin: 0 auto; }
    .header { text-align: center; margin-bottom: 22px; }
    .header-label {
      display: inline-block;
      background: var(--green); color: #fff;
      font-size: 10.5px; font-weight: 700; letter-spacing: 1.5px;
      padding: 4px 14px; border-radius: 20px; margin-bottom: 10px;
      box-shadow: 3px 3px 0 rgba(100,170,106,.35);
      transform: rotate(-1.5deg);
    }
    .header-label::before { content: '🌿'; margin-right: 4px; }
    .church-name {
      font-family: 'Noto Serif KR', serif;
      font-size: 42px; font-weight: 900; color: var(--text);
      letter-spacing: -1px; line-height: 1; margin-bottom: 4px;
    }
    .church-sub { font-size: 9.5px; letter-spacing: 4.5px; color: var(--soft); margin-bottom: 16px; }
    .title-pill {
      display: inline-flex; align-items: center; gap: 6px;
      background: var(--text); color: #fff;
      font-size: 14.5px; font-weight: 700;
      padding: 9px 22px; border-radius: 50px;
      box-shadow: 4px 4px 0 rgba(58,46,38,.18);
    }
    .date-row { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin: 14px 0 22px; }
    .date-sticker {
      background: var(--yellow-bg); border: 2px solid var(--yellow);
      color: var(--text); font-size: 11px; font-weight: 700;
      padding: 5px 14px; border-radius: 20px;
      box-shadow: 2px 3px 0 rgba(245,200,66,.3);
    }
    .date-sticker.soft {
      background: #fff; border-color: var(--border);
      color: var(--soft); font-weight: 400;
      box-shadow: 2px 3px 0 rgba(0,0,0,.05);
    }
    .card {
      background: var(--white); border-radius: 22px; padding: 20px; margin-bottom: 14px;
      box-shadow: 0 6px 24px rgba(0,0,0,.06), 0 1px 3px rgba(0,0,0,.04);
    }
    .sec-head { display: flex; align-items: center; gap: 11px; margin-bottom: 16px; }
    .sec-icon {
      width: 44px; height: 44px; border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px; flex-shrink: 0;
      box-shadow: 2px 4px 8px rgba(0,0,0,.10);
    }
    .sec-icon.green  { background: var(--green-bg); }
    .sec-title { font-size: 16px; font-weight: 700; }
    .sec-badge {
      margin-left: auto; font-size: 10px; font-weight: 700;
      padding: 3px 11px; border-radius: 20px;
      background: var(--green-bg); border: 1.5px solid var(--green); color: #388E3C;
      box-shadow: 1px 2px 0 rgba(0,0,0,.07);
    }
    .dawn-table { width: 100%; border-collapse: separate; border-spacing: 0 5px; font-size: 11.5px; }
    .dawn-table thead th {
      text-align: center; font-size: 10px; font-weight: 700;
      color: var(--soft); padding: 0 3px 6px;
    }
    .dawn-table thead th small { display: block; font-size: 9px; font-weight: 400; margin-top: 1px; }
    .dawn-table tbody td {
      padding: 7px 3px; text-align: center;
      background: #FAFAF8;
      border-top: 1.5px solid var(--border); border-bottom: 1.5px solid var(--border);
    }
    .dawn-table tbody td:first-child {
      border-left: 1.5px solid var(--border);
      border-radius: 10px 0 0 10px; padding-left: 8px;
    }
    .dawn-table tbody td:last-child {
      border-right: 1.5px solid var(--border);
      border-radius: 0 10px 10px 0; padding-right: 6px;
    }
    .row-label { font-size: 10px; font-weight: 700; color: var(--soft); white-space: nowrap; }
    .chip {
      display: inline-block; padding: 3px 7px; border-radius: 10px;
      font-size: 10.5px; font-weight: 700; line-height: 1.4;
      box-shadow: 1px 2px 0 rgba(0,0,0,.08);
    }
    .chip-pastor  { background: var(--pink-bg);   border: 1.5px solid var(--pink);   color: #C2185B; }
    .chip-sermon  { background: var(--yellow-bg);  border: 1.5px solid var(--yellow); color: #C77800; }
    .chip-sub     { background: var(--purple-bg);  border: 1.5px solid var(--purple); color: #512DA8; }
    .chip-plain   { background: #F5F3F0;           border: 1.5px solid #DDD8D0;       color: #5A4E44; }
    .nature-divider {
      text-align: center; font-size: 18px; letter-spacing: 10px;
      margin: 6px 0; opacity: 0.55; user-select: none;
    }
    .worship-grid { display: flex; gap: 12px; justify-content: center; }
    .worship-card {
      flex: 0 0 195px;
      background: var(--white); border-radius: 20px; overflow: hidden;
      box-shadow: 0 6px 24px rgba(0,0,0,.06), 0 1px 3px rgba(0,0,0,.04);
    }
    .worship-card-head { padding: 12px 12px 10px; }
    .worship-card-head.wed {
      background: linear-gradient(140deg, #EAF4FC 0%, #F3F8FF 100%);
      border-bottom: 2px dashed #BEE0F8;
    }
    .worship-card-head.fri {
      background: linear-gradient(140deg, #FFF8E8 0%, #FFFDF5 100%);
      border-bottom: 2px dashed #FFDFAA;
    }
    .worship-icon { font-size: 26px; margin-bottom: 5px; }
    .worship-title { font-size: 13px; font-weight: 700; }
    .worship-date { font-size: 10px; color: var(--soft); margin-top: 2px; font-weight: 500; }
    .worship-card-body { padding: 8px 10px; }
    .role-row {
      display: flex; align-items: center; gap: 8px;
      padding: 6px 0; border-bottom: 1.5px dashed #F0EDE8;
    }
    .role-row:last-child { border-bottom: none; }
    .role-tag {
      display: inline-block;
      font-size: 10.5px; font-weight: 700;
      padding: 2px 9px; border-radius: 8px;
      background: #FFF3E0; border: 1.5px solid #FFCC80; color: #E65100;
      white-space: nowrap; flex-shrink: 0;
      box-shadow: 1px 2px 0 rgba(230,81,0,.12);
    }
    .role-val { font-size: 13px; font-weight: 700; }
    .prayer-box {
      margin: 4px 10px 12px;
      background: var(--yellow-bg); border: 2px dashed var(--yellow);
      border-radius: 14px; padding: 9px 11px;
    }
    .prayer-title { font-size: 10px; font-weight: 700; color: #C77800; margin-bottom: 7px; }
    .prayer-title::before { content: '🙏 '; }
    .prayer-tags { display: flex; flex-wrap: wrap; gap: 5px; }
    .prayer-tag {
      background: #fff; border: 1.5px solid var(--yellow);
      color: var(--text); font-size: 10.5px; font-weight: 600;
      padding: 3px 9px; border-radius: 20px;
      box-shadow: 1px 2px 0 rgba(245,200,66,.25);
    }
    .footer {
      text-align: center; margin-top: 8px; padding: 16px;
      background: var(--white); border-radius: 18px; font-size: 10.5px;
      color: var(--soft); box-shadow: 0 4px 16px rgba(0,0,0,.04); line-height: 1.9;
    }
    .footer-badge {
      display: inline-flex; align-items: center; gap: 4px;
      background: var(--green-bg); border: 1.5px solid var(--green); color: #388E3C;
      font-size: 10.5px; font-weight: 700;
      padding: 4px 13px; border-radius: 20px; margin-bottom: 8px;
      box-shadow: 2px 2px 0 rgba(100,170,106,.2);
    }
    @media (max-width: 430px) {
      .church-name { font-size: 33px; }
      .worship-grid { grid-template-columns: 1fr; }
      body { padding: 20px 12px 44px; }
      .sec-icon { width: 38px; height: 38px; font-size: 20px; border-radius: 12px; }
    }
"""


def generate_html(dawn, wednesday, friday):
    month     = dawn.get('month', '?')
    start_day = dawn.get('start_day', '?')
    end_day   = dawn.get('end_day', '?')

    try:
        day_nums = list(range(int(start_day), int(end_day) + 1))
    except ValueError:
        day_nums = list(range(11, 17))
    day_headers = ''.join(
        f'<th>{DAYS_KR[i]}<small>{dn}일</small></th>'
        for i, dn in enumerate(day_nums[:6])
    )

    dawn_rows = ''
    for role in ['설교', '자막', '반주']:
        persons = dawn.get('roles', {}).get(role, [''] * 6)
        cells = ''.join(f'<td>{chip_html(p, role)}</td>' for p in persons[:6])
        dawn_rows += f'<tr><td><span class="row-label">{role}</span></td>{cells}</tr>\n'

    wed_roles_html = ''.join(
        f'<div class="role-row"><span class="role-tag">{r}</span><span class="role-val">{clean_name(v)}</span></div>'
        for r, v in wednesday.get('roles', {}).items()
    )
    fri_roles_html = ''.join(
        f'<div class="role-row"><span class="role-tag">{r}</span><span class="role-val">{clean_name(v)}</span></div>'
        for r, v in friday.get('roles', {}).items()
    )
    prayer_tags_html = ''.join(
        f'<span class="prayer-tag">{pw}</span>'
        for pw in friday.get('prayer_warriors', [])
    )

    wed_month = wednesday.get('month', month)
    wed_day   = wednesday.get('day', '?')
    fri_month = friday.get('month', month)
    fri_day   = friday.get('day', '?')
    badge        = f'{month}/{start_day} — {month}/{end_day}'
    date_display = f'{YEAR}년 {month}월 {start_day}일 — {month}월 {end_day}일'
    updated_at   = datetime.now().strftime('%Y-%m-%d %H:%M')

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>한 주간 예배 담당자 — 성민교회</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div class="title-pill">🌸 한 주간 예배 담당자</div>
  </div>
  <div class="date-row">
    <span class="date-sticker">🗓 {date_display}</span>
    <span class="date-sticker soft">자동 업데이트 {updated_at}</span>
  </div>
  <div class="card">
    <div class="sec-head">
      <div class="sec-icon green">🌅</div>
      <span class="sec-title">새벽기도회 담당</span>
      <span class="sec-badge">{badge}</span>
    </div>
    <table class="dawn-table">
      <thead><tr><th style="width:38px"></th>{day_headers}</tr></thead>
      <tbody>{dawn_rows}</tbody>
    </table>
  </div>
  <div class="nature-divider">🍃 🌿 🍃</div>
  <div class="worship-grid">
    <div class="worship-card">
      <div class="worship-card-head wed">
        <div class="worship-icon">🕊️</div>
        <div class="worship-title">수요예배</div>
        <div class="worship-date">{wed_month}월 {wed_day}일 (수)</div>
      </div>
      <div class="worship-card-body">{wed_roles_html}</div>
    </div>
    <div class="worship-card">
      <div class="worship-card-head fri">
        <div class="worship-icon">🔥</div>
        <div class="worship-title">금요성령집회</div>
        <div class="worship-date">{fri_month}월 {fri_day}일 (금)</div>
      </div>
      <div class="worship-card-body">{fri_roles_html}</div>
      <div class="prayer-box">
        <div class="prayer-title">기도용사</div>
        <div class="prayer-tags">{prayer_tags_html}</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div><span class="footer-badge">🌳 성민교회</span></div>
    사랑과 은혜가 넘치는 공동체<br>
    은혜로운 한 주간 되세요 🌸
  </div>
</div>
</body>
</html>"""


def main():
    if not NOTION_TOKEN:
        print('ERROR: NOTION_TOKEN 환경변수가 필요합니다.', file=sys.stderr)
        sys.exit(1)
    print('Notion 페이지 데이터 가져오는 중...')
    lines = fetch_lines()
    print(f'  → {len(lines)}줄 읽음')
    dawn, wednesday, friday = parse_all(lines)
    print(f'  → 새벽기도회: {dawn.get("month")}/{dawn.get("start_day")}-{dawn.get("end_day")}')
    print(f'  → 수요예배: {wednesday.get("month")}/{wednesday.get("day")}')
    print(f'  → 금요성령집회: {friday.get("month")}/{friday.get("day")}')
    html = generate_html(dawn, wednesday, friday)
    out_path = os.path.abspath(OUTPUT)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'worship.html 저장 완료: {out_path}')


if __name__ == '__main__':
    main()
