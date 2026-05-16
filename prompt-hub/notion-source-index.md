# Notion 원본 프롬프트 색인

원본 상위 페이지: `📜 여러 종류 프롬프트`

- URL: https://www.notion.so/2e05e604d8c6816b8355f9b7c004c32e
- 상위 경로: `AI agent` → `여러 종류 프롬프트`
- 용도: 목회 사역용 프롬프트 모음

## 1. 하네스 / 통합 실행

| 분류 | 제목 | Notion URL | GitHub 상태 |
|---|---|---|---|
| 하네스 | 새벽기도회용 하네스 | https://www.notion.so/3615e604d8c680b8b523d5245ccbd113 | 긴 원문. 색인 우선 생성 |

## 2. 설교 추천 / 연구 / 준비 / 작성

| 분류 | 제목 | Notion URL | 비고 |
|---|---|---|---|
| 설교 추천 | 설교 추천 프롬프트 | https://www.notion.so/2e05e604d8c681d1bc8ce3be25574496 | 단일 페이지 원문 확인됨 |
| 성경 연구 | 성경 연구 프롬프트 | https://www.notion.so/2e05e604d8c681c6a3bfeb73718730e7 | 하위 페이지 포함 |
| 설교 준비 | 설교 준비 프롬프트 모음 | https://www.notion.so/2e05e604d8c681e19edff601e850cdf3 | 다수 하위 페이지 포함 |
| 설교 작성 | 설교 작성 프롬프트 모음 | https://www.notion.so/2e05e604d8c681fe8ffbd6b1f587e3e2 | 다수 하위 페이지 포함 |
| 설교 진단 | 설교 진단 프롬프트 | https://www.notion.so/2e05e604d8c68130836bd4e7ad190a33 | 단일 페이지 원문 확인됨 |

## 3. 어린이 / 다음세대

| 분류 | 제목 | Notion URL | 비고 |
|---|---|---|---|
| 어린이 설교 | 어린이 설교 프롬프트 모음 | https://www.notion.so/2e05e604d8c6811c8a53e57352480f6b | 하위 페이지 포함 |

## 4. 기도 / 예배 / 목양

| 분류 | 제목 | Notion URL | 비고 |
|---|---|---|---|
| 대표기도 | 대표 기도 프롬프트 | https://www.notion.so/2e05e604d8c681cf91ffe7bf49531ca7 | 단일 페이지 원문 확인됨 |
| 장례설교 | 장례 설교 프롬프트 | https://www.notion.so/2e05e604d8c6816491e4f51a9153edde | 단일 페이지 원문 확인됨 |
| 장례기도 | 장례 기도 프롬프트 | https://www.notion.so/2e05e604d8c6818d9308cdf87fe7c71b | 단일 페이지 원문 확인됨 |
| 금요기도회 | 금요 기도회 인도 프롬프트 | https://www.notion.so/2e05e604d8c681d894e3e4068c22dade | 단일 페이지 원문 확인됨 |
| 양육 | 양육 프롬프트 | https://www.notion.so/2e05e604d8c6817889e7e2fb4a3f1925 | 단일 페이지 원문 확인됨 |
| 구역장 교육 | 구역장 교육 프롬프트 | https://www.notion.so/2e05e604d8c681eb9f45d8d7f5f586b1 | 단일 페이지 원문 확인됨 |
| 구역모임지 | 구역모임지 프롬프트 | https://www.notion.so/2e05e604d8c681dc8862e035d40eed6a | 단일 페이지 원문 확인됨 |
| 목회 계획 | 목회 계획 프롬프트 | https://www.notion.so/2e05e604d8c6819a92b4ce23a701ceb9 | 단일 페이지 원문 확인됨 |

## 5. 아이디어 / 제작 예정

| 분류 | 제목 | Notion URL | 비고 |
|---|---|---|---|
| 아이디어 | 만들고 싶은 프롬프트 | https://www.notion.so/2e05e604d8c681f489d9fa45b5693474 | 제작 예정 목록 |

## 마이그레이션 원칙

각 Notion 페이지는 GitHub에서 다음 형태로 옮기는 것을 권장합니다.

```markdown
---
id: unique-prompt-id
title: 프롬프트 제목
category: sermon | prayer | bible-study | pastoral-care | education | admin
source: notion
source_notion_url: https://www.notion.so/...
version: 0.1.0
last_migrated: 2026-05-16
---

# 프롬프트 제목

원문 프롬프트 내용...
```

## 주의사항

- API 키, Notion 토큰, OpenAI 키, 개인정보는 프롬프트 파일에 넣지 않습니다.
- 자동화에서 필요한 비밀값은 GitHub Secrets에 저장합니다.
- 원문을 수정할 때는 Notion과 GitHub 중 어느 쪽을 원본으로 삼을지 정해야 합니다.
- 추천: 앞으로는 GitHub를 원본, Notion을 운영 화면으로 사용합니다.
