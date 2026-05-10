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


# ── Notion API ─────────────────────────────────────────────────────────────

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


# ── Parsing ────────────────────────────────────────────────────────────────

def expand_days(s):
    """'월-화' → [0,1],  '월,목' → [0,3]"""
    s = s.strip()
    if '-' in s:
        a, b = s.split('-', 1)
        a, b = a.strip(), b.strip()
        if a in DAY_IDX and b in DAY_IDX:
            return list(range(DAY_IDX[a], DAY_IDX[b] + 1))
    return [DAY_IDX[d.strip()] for d in s.split(',') if d.strip() in DAY_IDX]


def parse_dawn_row(line):
    """설교: 윤수신 목사(월-화), 담임목사님(수-목) → ('설교', [name×6])"""
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


# ── Helpers ────────────────────────────────────────────────────────────────

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
        css = 'chip-rose'
    elif role == '설교':
        css = 'chip-gold'
    elif role == '자막':
        css = 'chip-lav'
    else:
        css = 'chip-plain'
    return f'<span class="chip {css}">{name}</span>'


# ── HTML generation ────────────────────────────────────────────────────────

CSS = """
    :root {
      --paper:      #FDF9F0;
      --paper-dark: #F2EAD3;
      --paper-mid:  #E8DBBF;
      --ink:        #1A0E0A;
      --ink-mid:    #4A2C1C;
      --ink-soft:   #8B6B4B;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #D4C5A0;
      background-image:
        repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(0,0,0,.04) 24px, rgba(0,0,0,.04) 25px),
        repeating-linear-gradient(90deg, transparent, transparent 24px, rgba(0,0,0,.04) 24px, rgba(0,0,0,.04) 25px);
      font-family: 'Noto Serif KR', serif;
      color: var(--ink);
      min-height: 100vh;
      padding: 20px 12px 40px;
    }
    .newspaper {
      max-width: 640px; margin: 0 auto;
      background: var(--paper);
      border: 2px solid var(--ink);
      box-shadow: 5px 5px 0 #A08860, 10px 10px 0 #C4AA80;
    }
    .masthead { padding: 18px 24px 14px; border-bottom: 4px double var(--ink); }
    .masthead-meta {
      display: flex; justify-content: space-between; align-items: center;
      font-family: 'Noto Sans KR', sans-serif; font-size: 9.5px;
      color: var(--ink-soft); letter-spacing: 0.5px;
      margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--paper-mid);
    }
    .masthead-center { text-align: center; }
    .church-name { font-size: 44px; font-weight: 900; letter-spacing: -2px; line-height: 1; color: var(--ink); }
    .church-sub { font-family: 'Noto Sans KR', sans-serif; font-size: 10px; letter-spacing: 4px; color: var(--ink-mid); margin-top: 5px; }
    .headline-block {
      background: var(--ink); color: var(--paper);
      text-align: center; padding: 10px 20px;
      font-size: 17px; font-weight: 700; letter-spacing: 1px;
    }
    .date-strip {
      display: flex; justify-content: space-between; align-items: center;
      padding: 7px 18px; background: var(--paper-dark);
      border-bottom: 1px solid var(--ink);
      font-family: 'Noto Sans KR', sans-serif; font-size: 10.5px; color: var(--ink-mid);
    }
    .content { padding: 22px 20px 20px; }
    .sec-head {
      display: flex; align-items: baseline; gap: 8px;
      border-bottom: 2.5px solid var(--ink); padding-bottom: 7px; margin-bottom: 14px;
    }
    .sec-icon { font-size: 17px; }
    .sec-title { font-size: 17px; font-weight: 700; letter-spacing: 0.3px; }
    .sec-badge {
      margin-left: auto; font-family: 'Noto Sans KR', sans-serif;
      font-size: 10px; font-weight: 600;
      color: var(--paper); background: var(--ink-mid);
      border: 1px solid var(--ink); border-radius: 20px; padding: 2px 10px;
    }
    .table-wrap { border: 1px solid var(--ink); border-radius: 2px; overflow: hidden; }
    table.dawn { width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 11px; }
    table.dawn thead tr { background: var(--ink); color: var(--paper); }
    table.dawn th {
      padding: 7px 2px; text-align: center;
      font-family: 'Noto Sans KR', sans-serif; font-weight: 500; font-size: 11px;
      border-right: 1px solid #3A2010;
    }
    table.dawn th:last-child { border-right: none; }
    table.dawn th small { display: block; font-size: 9px; opacity: 0.7; font-weight: 300; }
    table.dawn td {
      padding: 7px 2px; text-align: center;
      border-right: 1px solid #E0D0B8; border-bottom: 1px solid #E0D0B8; vertical-align: middle;
    }
    table.dawn td:last-child { border-right: none; }
    table.dawn tr:last-child td { border-bottom: none; }
    table.dawn tr:nth-child(even) td { background: var(--paper-dark); }
    table.dawn td.role {
      font-family: 'Noto Sans KR', sans-serif; font-weight: 700; font-size: 10px;
      color: var(--ink-mid); text-align: center; padding: 4px 2px;
      border-right: 1.5px solid var(--paper-mid);
      background: #F0E8D0 !important; white-space: nowrap;
    }
    .chip {
      display: inline-block; border-radius: 6px; padding: 2px 4px;
      font-size: 10px; font-family: 'Noto Sans KR', sans-serif;
      line-height: 1.3; word-break: keep-all;
    }
    .chip-gold  { background: var(--ink);        border: 1px solid var(--ink);        color: var(--paper); }
    .chip-rose  { background: var(--ink-mid);    border: 1px solid var(--ink-mid);    color: var(--paper); }
    .chip-lav   { background: #7A5C48;           border: 1px solid #7A5C48;           color: var(--paper); }
    .chip-plain { background: var(--paper-dark); border: 1px solid var(--paper-mid);  color: var(--ink-mid); }
    .fancy-div {
      display: flex; align-items: center; gap: 10px;
      margin: 20px 0; color: var(--ink-soft); font-size: 13px;
    }
    .fancy-div::before, .fancy-div::after {
      content: ''; flex: 1; height: 1px;
      background: linear-gradient(to right, transparent, var(--paper-mid), var(--ink-soft), var(--paper-mid), transparent);
    }
    .cards-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .card { border: 1.5px solid var(--ink); border-radius: 3px; overflow: hidden; }
    .card-head { background: var(--ink); color: var(--paper); padding: 9px 13px; }
    .card-head-title { font-size: 13.5px; font-weight: 700; letter-spacing: 0.3px; }
    .card-head-date { font-family: 'Noto Sans KR', sans-serif; font-size: 10px; margin-top: 2px; opacity: 0.7; }
    .card-body { padding: 10px 12px; }
    .role-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 6px 0; border-bottom: 1px dashed #D8C8A8; font-size: 12.5px;
    }
    .role-row:last-child { border-bottom: none; }
    .role-lbl { font-family: 'Noto Sans KR', sans-serif; font-size: 10px; font-weight: 700; color: var(--ink-soft); min-width: 28px; }
    .role-val { font-size: 12.5px; font-weight: 600; }
    .prayer-box {
      margin: 10px 12px 12px; background: var(--paper-dark);
      border: 1px solid var(--paper-mid); border-radius: 4px; padding: 8px 10px;
    }
    .prayer-title { font-family: 'Noto Sans KR', sans-serif; font-size: 10px; font-weight: 700; color: var(--ink-mid); margin-bottom: 6px; }
    .prayer-tags { display: flex; flex-wrap: wrap; gap: 4px; }
    .prayer-tag {
      font-family: 'Noto Sans KR', sans-serif; font-size: 10.5px;
      color: var(--ink-mid); background: var(--paper);
      border: 1px solid var(--ink-soft); border-radius: 20px; padding: 2px 9px;
    }
    .footer {
      border-top: 4px double var(--ink); padding: 12px 20px; text-align: center;
      font-family: 'Noto Sans KR', sans-serif; font-size: 10px;
      color: var(--ink-soft); background: var(--paper-dark); line-height: 1.7;
    }
    .footer strong { color: var(--ink-mid); }
    @media (max-width: 420px) {
      .church-name { font-size: 34px; }
      .cards-row { grid-template-columns: 1fr; }
      .masthead-meta { font-size: 8px; }
      .date-strip { font-size: 9.5px; padding: 6px 12px; }
      .content { padding: 16px 14px; }
    }
"""


def generate_html(dawn, wednesday, friday):
    month     = dawn.get('month', '?')
    start_day = dawn.get('start_day', '?')
    end_day   = dawn.get('end_day', '?')

    # Day column headers
    try:
        day_nums = list(range(int(start_day), int(end_day) + 1))
    except ValueError:
        day_nums = list(range(11, 17))
    day_headers = ''.join(
        f'<th>{DAYS_KR[i]}<small>{dn}일</small></th>'
        for i, dn in enumerate(day_nums[:6])
    )

    # Dawn table rows
    dawn_rows = ''
    for role in ['설교', '자막', '반주']:
        persons = dawn.get('roles', {}).get(role, [''] * 6)
        cells = ''.join(f'<td>{chip_html(p, role)}</td>' for p in persons[:6])
        dawn_rows += f'<tr><td class="role">{role}</td>{cells}</tr>\n'

    # Wednesday card
    wed_roles_html = ''.join(
        f'<div class="role-row"><span class="role-lbl">{r}</span><span class="role-val">{clean_name(v)}</span></div>'
        for r, v in wednesday.get('roles', {}).items()
    )

    # Friday card
    fri_roles_html = ''.join(
        f'<div class="role-row"><span class="role-lbl">{r}</span><span class="role-val">{clean_name(v)}</span></div>'
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
    meta_date    = f'✝ {YEAR}년 {month}월 {start_day}일(월) — {end_day}일(토)'
    updated_at   = datetime.now().strftime('%Y-%m-%d %H:%M')

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>한 주간 예배 담당자 — 성민교회</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
<div class="newspaper">

  <div class="masthead">
    <div class="masthead-meta">
      <span>{meta_date}</span>
      <span>매일의 향기</span>
      <span>자동 업데이트 {updated_at}</span>
    </div>
    <div class="masthead-center">
      <div class="church-name">성민교회</div>
      <div class="church-sub">S U N G M I N &nbsp; C H U R C H</div>
    </div>
  </div>

  <div class="headline-block">💯 한 주간 예배 담당자</div>

  <div class="date-strip">
    <span>🗓 {date_display}</span>
    <span>은혜로운 한 주간 되세요 🌸</span>
  </div>

  <div class="content">

    <div class="sec-head">
      <span class="sec-icon">🌅</span>
      <span class="sec-title">새벽기도회 담당</span>
      <span class="sec-badge">{badge}</span>
    </div>

    <div class="table-wrap">
      <table class="dawn">
        <thead>
          <tr>
            <th style="width:40px">역할</th>
            {day_headers}
          </tr>
        </thead>
        <tbody>
          {dawn_rows}
        </tbody>
      </table>
    </div>

    <div class="fancy-div">✦ &nbsp; ✦ &nbsp; ✦</div>

    <div class="sec-head">
      <span class="sec-icon">🕊</span>
      <span class="sec-title">주중 예배 담당</span>
    </div>

    <div class="cards-row">

      <div class="card">
        <div class="card-head">
          <div class="card-head-title">🕊 수요예배</div>
          <div class="card-head-date">{wed_month}월 {wed_day}일 (수)</div>
        </div>
        <div class="card-body">
          {wed_roles_html}
        </div>
      </div>

      <div class="card">
        <div class="card-head">
          <div class="card-head-title">🔥 금요성령집회</div>
          <div class="card-head-date">{fri_month}월 {fri_day}일 (금)</div>
        </div>
        <div class="card-body">
          {fri_roles_html}
        </div>
        <div class="prayer-box">
          <div class="prayer-title">🙏 기도용사</div>
          <div class="prayer-tags">{prayer_tags_html}</div>
        </div>
      </div>

    </div>

  </div>

  <div class="footer">
    <strong>✝ 성민교회</strong> — 사랑과 은혜가 넘치는 공동체<br>
    매일의 향기와 함께하는 신앙생활 🌸
  </div>

</div>
</body>
</html>"""


# ── Main ───────────────────────────────────────────────────────────────────

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
