# 프롬프트

목회 사역용 프롬프트를 GitHub에서 관리하기 위한 저장소입니다.

원본은 Notion의 `📜 여러 종류 프롬프트` 페이지이며, 이 저장소는 해당 프롬프트 모음을 앱·자동화·AI 작업에서 안정적으로 불러오기 위한 GitHub 버전입니다.

- Notion 원본: https://www.notion.so/2e05e604d8c6816b8355f9b7c004c32e
- 현재 GitHub 저장소: `Jeong-ZeeWon/sungminchurch`
- 권장 저장소명: `prompt` 또는 `prompts`

## 이 저장소의 목적

이 저장소는 다음 목회 작업을 위한 프롬프트를 보관합니다.

1. 새벽기도회 설교 준비 하네스
2. 설교 유형 추천
3. 성경 연구 프롬프트
4. 설교 준비 프롬프트
5. 설교 작성 프롬프트
6. 설교 진단 프롬프트
7. 대표기도 프롬프트
8. 장례 설교·기도 프롬프트
9. 금요기도회 인도 프롬프트
10. 어린이 설교 프롬프트
11. 목회 계획·양육·구역모임 프롬프트

## 기본 구조

```text
README.md
notion-source-index.md
categories/
  bible-study-index.md
  sermon-preparation-index.md
  sermon-writing-index.md
  children-sermon-index.md
  prayer-and-pastoral-index.md
prompts/
  sermon-recommendation.md
  representative-prayer.md
  funeral-sermon.md
  funeral-prayer.md
  friday-prayer-meeting.md
  sermon-diagnosis.md
  pastoral-plan.md
  cell-leader-training.md
  cell-meeting-guide.md
templates/
  prompt-file-template.md
  ai-execution-template.md
```

## 추천 사용 방식

### 1. 직접 복사해서 사용

필요한 프롬프트 파일을 열고 내용을 ChatGPT, Claude, Gemini 등에 붙여 넣습니다.

### 2. 앱에서 Raw URL로 불러오기

프롬프트 파일을 앱에서 불러올 때는 Raw URL을 사용합니다.

```text
https://raw.githubusercontent.com/Jeong-ZeeWon/sungminchurch/main/prompts/sermon-recommendation.md
```

### 3. Notion과 함께 사용

추천 구조는 다음과 같습니다.

```text
Notion = 작업 목록, 본문, 예배 정보, 결과물 저장
GitHub = 프롬프트 원본, 버전 관리, 자동화 코드
AI = GitHub 프롬프트 + Notion 입력값을 받아 결과 생성
```

## 운영 원칙

- GitHub를 프롬프트 원본 저장소로 사용합니다.
- Notion은 보기 좋은 운영 화면과 결과물 저장소로 사용합니다.
- 중요한 프롬프트 수정은 반드시 커밋 메시지에 이유를 남깁니다.
- API 키, Notion 토큰, OpenAI 키 등 비밀 정보는 저장소에 넣지 않습니다.
- 자동화에 필요한 비밀값은 GitHub Secrets에 저장합니다.

## 다음 단계

- Notion Markdown Export 파일을 업로드하면 각 하위 페이지 원문을 개별 `.md` 파일로 1:1 분리할 수 있습니다.
- 특히 `새벽기도회용 하네스`처럼 긴 문서는 Notion API 응답이 일부 잘릴 수 있으므로 Export 파일 기반 이전이 가장 안전합니다.
