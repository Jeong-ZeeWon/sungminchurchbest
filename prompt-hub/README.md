# 목회 프롬프트 허브

이 폴더는 Notion의 `📜 여러 종류 프롬프트` 페이지를 GitHub에서 관리하고 활용하기 위한 프롬프트 허브입니다.

- 원본 Notion 페이지: https://www.notion.so/2e05e604d8c6816b8355f9b7c004c32e
- GitHub 저장 위치: `prompt-hub/`
- 목적: 설교 연구, 설교 작성, 기도문, 목회 계획, 양육, 구역모임, 장례, 금요기도회 등 목회 사역용 프롬프트를 버전 관리하고 앱/자동화에서 불러와 사용할 수 있도록 정리합니다.

## 기본 원칙

1. **Notion은 운영 화면**으로 사용합니다.
   - 프롬프트 목록 보기
   - 목회 작업 흐름 관리
   - 결과물 저장

2. **GitHub는 원본 관리소**로 사용합니다.
   - 프롬프트 버전 관리
   - 변경 이력 추적
   - 앱/자동화에서 Raw 파일로 불러오기
   - Notion API, OpenAI API, Claude, 자동화 스크립트와 연결

3. **긴 원문 프롬프트는 Notion 원문 링크를 병행 보존합니다.**
   - 일부 Notion 페이지는 내용이 매우 길어 도구 응답이 중간에서 잘릴 수 있습니다.
   - GitHub에는 우선 안정적인 색인, 분류, 활용 지침을 저장하고, 이후 Notion Markdown Export 파일을 업로드하면 원문 전체를 1:1로 마이그레이션할 수 있습니다.

## 폴더 구조

```text
prompt-hub/
  README.md
  notion-source-index.md
  categories/
    bible-study-index.md
    sermon-preparation-index.md
    sermon-writing-index.md
    children-sermon-index.md
  summaries/
    major-prompt-summaries.md
  templates/
    prompt-file-template.md
```

## 활용 방식

### 1. 사람이 직접 사용할 때

GitHub에서 필요한 프롬프트 파일을 열고 복사하여 ChatGPT, Claude, Gemini 등에 붙여 넣습니다.

### 2. 앱에서 사용할 때

프롬프트 파일의 Raw URL을 앱 코드에서 불러옵니다.

예시:

```text
https://raw.githubusercontent.com/Jeong-ZeeWon/sungminchurch/main/prompt-hub/README.md
```

### 3. Notion과 함께 사용할 때

- Notion: 본문, 예배 유형, 작업 상태, 결과물 관리
- GitHub: 프롬프트 원본, 버전, 자동화 코드 관리

추천 흐름:

```text
Notion 작업 항목 생성
→ GitHub에서 해당 프롬프트 Raw 파일 불러오기
→ AI 실행
→ 결과를 Notion 페이지에 저장
→ GitHub에서 프롬프트 버전 개선
```

## 다음 단계

1. Notion에서 `📜 여러 종류 프롬프트` 페이지를 Markdown/CSV로 Export합니다.
2. Export된 `.zip` 파일을 업로드합니다.
3. 각 프롬프트 원문을 GitHub의 개별 `.md` 파일로 1:1 분리합니다.
4. `version`, `category`, `target`, `source_notion_url` 같은 YAML 메타데이터를 추가합니다.
5. 앱에서 선택형 프롬프트 실행 구조로 연결합니다.
