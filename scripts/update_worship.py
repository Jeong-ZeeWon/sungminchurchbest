#!/usr/bin/env python3
"""
update_worship.py  -  매주 토요일 GitHub Actions에서 실행
노션 담당자 페이지 → worship.html 자동 업데이트
"""
import os, re, requests
from datetime import datetime, timedelta

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

DAWN_PAGE = "2df5e604d8c68142b803c8ada553a6ae"
WED_PAGE  = "2e15e604d8c6802f8284dd7ccc553b4f"
FRI_PAGE  = "2e35e604d8c681df8d57cdbab62ed6ec"

# 날짜 계산 (KST)
now = datetime.utcnow() + timedelta(hours=9)
wd  = now.weekday()  # 0=Mon, 5=Sat, 6=Sun
if wd == 5:   days_to_mon = 2
elif wd == 6: days_to_mon = 1
else:         days_to_mon = (7 - wd) % 7 or 7

next_mon = now + timedelta(days=days_to_mon)
week = [next_mon + timedelta(days=i) for i in range(6)]

def mdd(d): return f"{d.month}/{d.day:02d}"
def md(d):  return f"{d.month}/{d.day}"

DAWN_DATES = [mdd(d) for d in week]
WED_DATE   = mdd(week[2])
FRI_DATE   = md(week[4])
DAYS       = ["월","화","수","목","금","토"]

# Notion API
def get_text(rt):
    return "".join(r.get("plain_text","") for r in rt).strip()

def get_blocks(bid):
    url, params, out = f"https://api.notion.com/v1/blocks/{bid}/children", {"page_size":100}, []
    while True:
        r = requests.get(url, headers=HEADERS, params=params).json()
        out += r.get("results", [])
        if not r.get("has_more"): break
        params["start_cursor"] = r["next_cursor"]
    return out

def table_rows(tid):
    rows = []
    for b in get_blocks(tid):
        if b["type"] == "table_row":
            rows.append([get_text(c) for c in b["table_row"]["cells"]])
    return rows

def page_tables(pid):
    return [table_rows(b["id"]) for b in get_blocks(pid) if b["type"] == "table"]

# 새벽기도회
def find_dawn_table(tables):
    for t in tables:
        for row in t:
            if row and row[0] == "날짜" and len(row) > 1 and row[1] == DAWN_DATES[0]:
                return t
    return None

dawn_raw = {"설교":[""]* 6, "자막":[""]* 6, "반주":[""]* 6}
dawn_t = find_dawn_table(page_tables(DAWN_PAGE))
if dawn_t:
    for row in dawn_t:
        role = row[0].strip() if row else ""
        if role in dawn_raw:
            dawn_raw[role] = [(row[i+1].strip() if i+1 < len(row) else "") for i in range(6)]

def add_pastor(n):
    n = n.strip()
    if not n: return "미등록"
    if n in ("담임목사님","목사님"): return n
    if n.endswith(("목사","목사님")): return n
    return n + " 목사"

def group_days(names):
    groups, i = [], 0
    while i < 6:
        if not names[i]: i += 1; continue
        n, j = names[i], i + 1
        while j < 6 and names[j] == n: j += 1
        idx = list(range(i, j))
        if len(idx) == 1:
            tag = DAYS[idx[0]]
        elif idx == list(range(idx[0], idx[-1]+1)):
            tag = f"{DAYS[idx[0]]}-{DAYS[idx[-1]]}"
        else:
            tag = ",".join(DAYS[k] for k in idx)
        groups.append((n, tag)); i = j
    return groups

# 수요예배
def clean_name(n):
    n = re.sub(r'\s*\d+-?\d*$', '', n).strip()
    n = re.sub(r'\s*(목사|권사|전도사|사모|장로|집사|담임)$', '', n).strip()
    return n or "미등록"

wed = {"설교":"미등록","찬양":"미등록","음향":"미등록","PD":"미등록"}
for t in page_tables(WED_PAGE):
    for row in t:
        if len(row) >= 4 and row[1].strip() == WED_DATE:
            if len(row)>3: wed["설교"] = clean_name(row[3])
            if len(row)>4: wed["찬양"] = clean_name(row[4])
            if len(row)>5: wed["음향"] = clean_name(row[5])
            if len(row)>6: wed["PD"]   = clean_name(row[6])
            break

# 금요성령집회
fri = {"찬양":"미등록","PD":"미등록","자막":"미등록","기도용사":[]}
for t in page_tables(FRI_PAGE):
    if not t or not t[0] or t[0][0].strip() != "날짜": continue
    for row in t[1:]:
        if row and row[0].strip() == FRI_DATE:
            if len(row)>1: fri["찬양"] = row[1].strip()
            if len(row)>2: fri["PD"]   = row[2].strip()
            if len(row)>3: fri["자막"] = row[3].strip()
            if len(row)>4: fri["기도용사"] = row[4].strip().split()
            break

# HTML 생성
s, e = week[0], week[5]
wed_label = f"{week[2].month}/{week[2].day}(수)"
fri_label = f"{week[4].month}/{week[4].day}(금)"
updated   = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")

def chip(v, cls):
    return f'<span class="chip chip-{cls}">{v}</span>'

def dawn_row(role, values, fmt, cls):
    cells = "".join(f'<td>{chip(fmt(v), cls)}</td>' for v in values)
    return f'<tr><td class="role">{role}</td>{cells}</tr>'

prayer_tags = "".join(f'<span class="prayer-tag">{p}</span>' for p in fri["기도용사"])
th_days = "".join(f'<th>{DAYS[i]}<small>{week[i].day}일</small></th>' for i in range(6))

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>한 주간 예배 담당자 — 성민교회</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --paper:      #FDF9F0;
      --paper-dark: #F2EAD3;
      --paper-mid:  #E8DBBF;
      --ink:        #1A0E0A;
      --ink-mid:    #4A2C1C;
      --ink-soft:   #8B6B4B;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #D4C5A0;
      background-image:
        repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(0,0,0,.04) 24px, rgba(0,0,0,.04) 25px),
        repeating-linear-gradient(90deg, transparent, transparent 24px, rgba(0,0,0,.04) 24px, rgba(0,0,0,.04) 25px);
      font-family: 'Noto Serif KR', serif;
      color: var(--ink);
      min-height: 100vh;
      padding: 20px 12px 40px;
    }}
    .newspaper {{ max-width: 640px; margin: 0 auto; background: var(--paper); border: 2px solid var(--ink); box-shadow: 5px 5px 0 #A08860, 10px 10px 0 #C4AA80; }}
    .masthead {{ padding: 18px 24px 14px; border-bottom: 4px double var(--ink); }}
    .masthead-meta {{ display: flex; justify-content: space-between; align-items: center; font-family: 'Noto Sans KR', sans-serif; font-size: 9.5px; color: var(--ink-soft); letter-spacing: 0.5px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--paper-mid); }}
    .masthead-center {{ text-align: center; }}
    .church-name {{ font-size: 44px; font-weight: 900; letter-spacing: -2px; line-height: 1; color: var(--ink); }}
    .church-sub {{ font-family: 'Noto Sans KR', sans-serif; font-size: 10px; letter-spacing: 4px; color: var(--ink-mid); margin-top: 5px; }}
    .headline-block {{ background: var(--ink); color: var(--paper); text-align: center; padding: 10px 20px; font-size: 17px; font-weight: 700; letter-spacing: 1px; }}
    .date-strip {{ display: flex; justify-content: space-between; align-items: center; padding: 7px 18px; background: var(--paper-dark); border-bottom: 1px solid var(--ink); font-family: 'Noto Sans KR', sans-serif; font-size: 10.5px; color: var(--ink-mid); }}
    .content {{ padding: 22px 20px 20px; }}
    .sec-head {{ display: flex; align-items: baseline; gap: 8px; border-bottom: 2.5px solid var(--ink); padding-bottom: 7px; margin-bottom: 14px; }}
    .sec-icon {{ font-size: 17px; }}
    .sec-title {{ font-size: 17px; font-weight: 700; letter-spacing: 0.3px; }}
    .sec-badge {{ margin-left: auto; font-family: 'Noto Sans KR', sans-serif; font-size: 10px; font-weight: 600; color: var(--paper); background: var(--ink-mid); border: 1px solid var(--ink); border-radius: 20px; padding: 2px 10px; }}
    .table-wrap {{ border: 1px solid var(--ink); border-radius: 2px; overflow: hidden; }}
    table.dawn {{ width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 11px; }}
    table.dawn thead tr {{ background: var(--ink); color: var(--paper); }}
    table.dawn th {{ padding: 7px 2px; text-align: center; font-family: 'Noto Sans KR', sans-serif; font-weight: 500; font-size: 11px; border-right: 1px solid #3A2010; }}
    table.dawn th:last-child {{ border-right: none; }}
    table.dawn th small {{ display: block; font-size: 9px; opacity: 0.7; font-weight: 300; }}
    table.dawn td {{ padding: 7px 2px; text-align: center; border-right: 1px solid #E0D0B8; border-bottom: 1px solid #E0D0B8; vertical-align: middle; }}
    table.dawn td:last-child {{ border-right: none; }}
    table.dawn tr:last-child td {{ border-bottom: none; }}
    table.dawn tr:nth-child(even) td {{ background: var(--paper-dark); }}
    table.dawn td.role {{ font-family: 'Noto Sans KR', sans-serif; font-weight: 700; font-size: 10px; color: var(--ink-mid); text-align: center; padding: 4px 2px; border-right: 1.5px solid var(--paper-mid); background: #F0E8D0 !important; white-space: nowrap; }}
    .chip {{ display: inline-block; border-radius: 6px; padding: 2px 4px; font-size: 10px; font-family: 'Noto Sans KR', sans-serif; line-height: 1.3; word-break: keep-all; }}
    .chip-gold  {{ background: var(--ink);        border: 1px solid var(--ink);        color: var(--paper); }}
    .chip-lav   {{ background: #7A5C48;           border: 1px solid #7A5C48;           color: var(--paper); }}
    .chip-plain {{ background: var(--paper-dark); border: 1px solid var(--paper-mid);  color: var(--ink-mid); }}
    .fancy-div {{ display: flex; align-items: center; gap: 10px; margin: 20px 0; color: var(--ink-soft); font-size: 13px; }}
    .fancy-div::before, .fancy-div::after {{ content: ''; flex: 1; height: 1px; background: linear-gradient(to right, transparent, var(--paper-mid), var(--ink-soft), var(--paper-mid), transparent); }}
    .cards-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .card {{ border: 1.5px solid var(--ink); border-radius: 3px; overflow: hidden; }}
    .card-head {{ background: var(--ink); color: var(--paper); padding: 9px 13px; }}
    .card-head-title {{ font-size: 13.5px; font-weight: 700; letter-spacing: 0.3px; }}
    .card-head-date {{ font-family: 'Noto Sans KR', sans-serif; font-size: 10px; margin-top: 2px; opacity: 0.7; }}
    .card-body {{ padding: 10px 12px; }}
    .role-row {{ display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #D8C8A8; font-size: 12.5px; }}
    .role-row:last-child {{ border-bottom: none; }}
    .role-lbl {{ font-family: 'Noto Sans KR', sans-serif; font-size: 10px; font-weight: 700; color: var(--ink-soft); min-width: 28px; }}
    .role-val {{ font-size: 12.5px; font-weight: 600; }}
    .prayer-box {{ margin: 10px 12px 12px; background: var(--paper-dark); border: 1px solid var(--paper-mid); border-radius: 4px; padding: 8px 10px; }}
    .prayer-title {{ font-family: 'Noto Sans KR', sans-serif; font-size: 10px; font-weight: 700; color: var(--ink-mid); margin-bottom: 6px; }}
    .prayer-tags {{ display: flex; flex-wrap: wrap; gap: 4px; }}
    .prayer-tag {{ font-family: 'Noto Sans KR', sans-serif; font-size: 10.5px; color: var(--ink-mid); background: var(--paper); border: 1px solid var(--ink-soft); border-radius: 20px; padding: 2px 9px; }}
    .footer {{ border-top: 4px double var(--ink); padding: 12px 20px; text-align: center; font-family: 'Noto Sans KR', sans-serif; font-size: 10px; color: var(--ink-soft); background: var(--paper-dark); line-height: 1.7; }}
    .footer strong {{ color: var(--ink-mid); }}
    @media (max-width: 420px) {{ .church-name {{ font-size: 34px; }} .cards-row {{ grid-template-columns: 1fr; }} .masthead-meta {{ font-size: 8px; }} .date-strip {{ font-size: 9.5px; padding: 6px 12px; }} .content {{ padding: 16px 14px; }} }}
  </style>
</head>
<body>
<div class="newspaper">
  <div class="masthead">
    <div class="masthead-meta">
      <span>✝ {s.year}년 {s.month}월 {s.day}일(월) — {e.day}일(토)</span>
      <span>매일의 향기</span>
      <span>자동 업데이트 {updated}</span>
    </div>
    <div class="masthead-center">
      <div class="church-name">성민교회</div>
      <div class="church-sub">S U N G M I N &nbsp; C H U R C H</div>
    </div>
  </div>
  <div class="headline-block">💯 한 주간 예배 담당자</div>
  <div class="date-strip">
    <span>🗓 {s.year}년 {s.month}월 {s.day}일 — {e.month}월 {e.day}일</span>
    <span>은혜로운 한 주간 되세요 🌸</span>
  </div>
  <div class="content">
    <div class="sec-head">
      <span class="sec-icon">🌅</span>
      <span class="sec-title">새벽기도회 담당</span>
      <span class="sec-badge">{s.month}/{s.day} — {e.month}/{e.day}</span>
    </div>
    <div class="table-wrap">
      <table class="dawn">
        <thead><tr><th style="width:40px">역할</th>{th_days}</tr></thead>
        <tbody>
          {dawn_row("설교", dawn_raw["설교"], add_pastor, "gold")}
          {dawn_row("자막", dawn_raw["자막"], add_pastor, "lav")}
          {dawn_row("반주", dawn_raw["반주"], lambda x: x.strip() or "미등록", "plain")}
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
          <div class="card-head-date">{wed_label}</div>
        </div>
        <div class="card-body">
          <div class="role-row"><span class="role-lbl">설교</span><span class="role-val">{wed["설교"]}</span></div>
          <div class="role-row"><span class="role-lbl">찬양</span><span class="role-val">{wed["찬양"]}</span></div>
          <div class="role-row"><span class="role-lbl">음향</span><span class="role-val">{wed["음향"]}</span></div>
          <div class="role-row"><span class="role-lbl">PD</span><span class="role-val">{wed["PD"]}</span></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">
          <div class="card-head-title">🔥 금요성령집회</div>
          <div class="card-head-date">{fri_label}</div>
        </div>
        <div class="card-body">
          <div class="role-row"><span class="role-lbl">찬양</span><span class="role-val">{fri["찬양"]}</span></div>
          <div class="role-row"><span class="role-lbl">PD</span><span class="role-val">{fri["PD"]}</span></div>
          <div class="role-row"><span class="role-lbl">자막</span><span class="role-val">{fri["자막"]}</span></div>
        </div>
        <div class="prayer-box">
          <div class="prayer-title">🙏 기도용사</div>
          <div class="prayer-tags">{prayer_tags}</div>
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
</html>'''

with open("worship.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ worship.html 업데이트 완료 ({updated})")
print(f"   새벽: {s.month}/{s.day}-{e.day}, 수요: {wed_label}, 금요: {fri_label}")

# ── index.html leadersData 업데이트 ─────────────
fri_prayer_list = fri["기도용사"] if isinstance(fri["기도용사"], list) else fri["기도용사"].split()

preacher_js = ",".join(f"'{v}'" for v in dawn_raw["설교"])
caption_js  = ",".join(f"'{v}'" for v in dawn_raw["자막"])
accomp_js   = ",".join(f"'{v}'" for v in dawn_raw["반주"])
prayer_js   = ",".join(f"'{p}'" for p in fri_prayer_list)

week_label  = f"{s.month}/{s.day} — {e.month}/{e.day}"

new_leaders = f"""const leadersData = {{
  week: '{week_label}',
  dawn: {{
    preacher: [{preacher_js}],
    caption:  [{caption_js}],
    accomp:   [{accomp_js}],
  }},
  days: ['월','화','수','목','금','토'],
  wed: {{ date:'{wed_label}', preacher:'{wed["설교"]}', worship:'{wed["찬양"]}', sound:'{wed["음향"]}', pd:'{wed["PD"]}' }},
  fri: {{ date:'{fri_label}(금)', worship:'{fri["찬양"]}', pd:'{fri["PD"]}', caption:'{fri["자막"]}', prayer:[{prayer_js}] }},
}};"""

START = "// LEADERS_DATA_START\n"
END   = "\n// LEADERS_DATA_END"
try:
    with open("index.html", "r", encoding="utf-8") as f:
        idx_html = f.read()
    s_pos = idx_html.index(START) + len(START)
    e_pos = idx_html.index(END, s_pos)
    idx_html = idx_html[:s_pos] + new_leaders + idx_html[e_pos:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(idx_html)
    print(f"✅ index.html leadersData 업데이트 완료")
except Exception as ex:
    print(f"⚠️  index.html 업데이트 실패: {ex}")
