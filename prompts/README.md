# Prompts

이 폴더는 실제 실행용 프롬프트 파일을 보관합니다.

## 현재 생성된 파일

| 파일 | 용도 |
|---|---|
| `sermon-recommendation.md` | 본문과 주제에 맞는 설교 유형 추천 |
| `sermon-diagnosis.md` | 작성된 설교문 점검 및 개선 |

## 원문 이전 예정 파일

아래 파일들은 Notion 원문 또는 Markdown Export 파일을 기준으로 추가 이전할 예정입니다.

| 예정 파일 | 원본 |
|---|---|
| `representative-prayer.md` | 대표 기도 프롬프트 |
| `funeral-sermon.md` | 장례 설교 프롬프트 |
| `funeral-prayer.md` | 장례 기도 프롬프트 |
| `friday-prayer-meeting.md` | 금요 기도회 인도 프롬프트 |
| `pastoral-plan.md` | 목회 계획 프롬프트 |
| `cell-leader-training.md` | 구역장 교육 프롬프트 |
| `cell-meeting-guide.md` | 구역모임지 프롬프트 |

## 작성 원칙

각 파일은 다음 메타데이터를 포함하는 것을 권장합니다.

```yaml
id: prompt-id
title: title
category: sermon | prayer | bible-study | pastoral-care | education | admin
source_notion_url: https://www.notion.so/...
version: 0.1.0
```
