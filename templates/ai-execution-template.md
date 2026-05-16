# AI 실행 템플릿

아래 양식은 GitHub에 저장된 프롬프트를 AI에게 실행시킬 때 사용하는 입력 템플릿입니다.

## 실행 요청

```text
아래 GitHub Raw 링크의 프롬프트를 기준으로 작업해 주세요.

프롬프트 Raw URL:
[여기에 Raw URL]

입력값:
- 본문:
- 예배/사역 유형:
- 대상:
- 분량:
- 강조점:
- 참고자료:

출력 조건:
- 한국어 존댓말
- 예장 통합 목회 현장에 맞는 표현
- 본문 중심
- 실제 예배/사역 현장에서 사용할 수 있는 형태
```

## Notion 연동 실행 구조

```text
1. Notion DB에서 작업 항목을 읽습니다.
2. 항목의 카테고리에 맞는 GitHub 프롬프트 Raw URL을 선택합니다.
3. 프롬프트와 입력값을 AI에 전달합니다.
4. 결과물을 Notion 페이지에 저장합니다.
5. 상태를 '완료'로 변경합니다.
```

## Raw URL 예시

```text
https://raw.githubusercontent.com/Jeong-ZeeWon/sungminchurch/main/prompts/sermon-recommendation.md
```
