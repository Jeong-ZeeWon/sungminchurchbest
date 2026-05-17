# 성경 연구 프롬프트 색인

원본 Notion 페이지: https://www.notion.so/2e05e604d8c681c6a3bfeb73718730e7

성경 연구 프롬프트는 설교 작성 전 본문을 깊이 연구하기 위한 모듈입니다.

## 기본값

앞으로 사용자가 다음과 같이 말하면 반드시 `통합 연구 프롬프트`를 기본으로 사용합니다.

```text
성경 연구 프롬프트 전부
통합 연구 프롬프트 전부
전부 돌려줘
통합으로 해줘
```

기본 실행 파일:

```text
prompts/bible-study/integrated/00-integrated-bible-study-all.md
```

## 통합 연구 프롬프트

| 제목 | GitHub 파일 | Notion URL | 상태 |
|---|---|---|---|
| 통합 전체 실행 프롬프트 | `prompts/bible-study/integrated/00-integrated-bible-study-all.md` | https://www.notion.so/2e05e604d8c681df9ea2c680a75bae61 | 기본값 |
| 원어 연구 | `prompts/bible-study/integrated/01-original-language.md` | https://www.notion.so/2e05e604d8c68169808dc61694e5b714 | 이전 완료 |
| 구조 연구 | `prompts/bible-study/integrated/02-structure.md` | https://www.notion.so/2e05e604d8c681739f6ae819328dded4 | 이전 완료 |
| 신학 비교 | `prompts/bible-study/integrated/03-theological-comparison.md` | https://www.notion.so/2e05e604d8c681c1a79dfce80c4be749 | 실행용 버전 |
| 본문 비평 | `prompts/bible-study/integrated/04-textual-criticism.md` | https://www.notion.so/2e05e604d8c681e8912bccc541d4473c | 실행용 버전 |
| 비판적 사회 윤리 | `prompts/bible-study/integrated/05-social-ethical.md` | https://www.notion.so/2e05e604d8c681a18e25efdd8ac073e5 | 이전 완료 |
| 묵상 목회 적용 | `prompts/bible-study/integrated/06-pastoral-application.md` | https://www.notion.so/2e05e604d8c681f289ced2aa7d267221 | 이전 완료 |
| 다라쉬 | `prompts/bible-study/integrated/07-darash.md` | https://www.notion.so/2e05e604d8c681dabb03cd1c3c454b6f | 이전 완료 |
| 신학자 대화식 해석 | `prompts/bible-study/integrated/08-theologian-dialogue.md` | https://www.notion.so/2e05e604d8c681729f2ac1cc40c92511 | 실행용 버전 |
| 주석 | `prompts/bible-study/integrated/09-commentary.md` | https://www.notion.so/2e05e604d8c681248d83f703490f15c0 | 이전 완료 |
| 예화 | `prompts/bible-study/integrated/10-illustrations.md` | https://www.notion.so/2e05e604d8c68129afb1eb1214bd1bed | 이전 완료 |
| 설교 준비 통합 | `prompts/bible-study/integrated/11-sermon-preparation.md` | https://www.notion.so/2e05e604d8c6817da9b0f3258f1d0b16 | 이전 완료 |

## 개별 연구 프롬프트

개별 연구 프롬프트는 보조 자료로 둡니다. 사용자가 별도로 `개별 연구 프롬프트 전부`라고 요청할 때만 사용합니다.

Notion URL: https://www.notion.so/2e05e604d8c6813393a3f33208030463

## 저장 원칙

연구 결과는 기본적으로 `Jeong-ZeeWon/bible-research` 저장소에 저장합니다.

권장 경로:

```text
pericopes/{book-number-book-name}/{book-abbrev-chapter-verse}/
```

예시:

```text
pericopes/46-1corinthians/1co-12-12-20/
pericopes/01-genesis/gen-01-01/
```
