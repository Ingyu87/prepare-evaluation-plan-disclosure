# 평가계획 정보공시 스킬

초등학교 교수·학습 및 평가계획을 정보공시 개정 기준에 맞게 검토하고 개정하는 Agent Skill입니다. Codex와 Claude Code에서 사용할 수 있습니다.

## 주요 기능

- 공식 표제를 `단원명(교수·학습 내용)`, `평가 방법 및 횟수`, `성취수준`으로 정비
- `[토의·토론 수업]`, `[탐구 학습]` 같은 괄호형 수업 방법명 제거
- 실제 학습 활동을 교수·학습 내용으로 보존
- 성취수준을 `~할 수 있다`보다 `~한다·설명한다·표현한다` 형태로 정비
- HWP/HWPX 파일 변환 및 결과 검증 절차 제공

## 지원 환경

- HWPX 표제 수정: Python 3 표준 라이브러리
- HWP 자동 변환: Windows, PowerShell, 한컴오피스 설치 환경
- 한컴오피스 COM 자동화를 사용할 수 없는 환경에서는 HWPX 파일로 작업해야 합니다.

## Codex에서 사용

Codex에서 다음과 같이 요청해 설치할 수 있습니다.

```text
$skill-installer로 Ingyu87/prepare-evaluation-plan-disclosure 저장소의
skills/prepare-evaluation-plan-disclosure 스킬을 설치해 줘.
```

설치 후 다음처럼 호출합니다.

```text
$prepare-evaluation-plan-disclosure로 이 평가계획을 정보공시 기준에 맞게 검토하고 HWP로 만들어 줘.
```

## Claude Code에서 사용

개인 스킬로 설치하려면 저장소를 내려받은 뒤 다음 폴더를 복사합니다.

```text
skills/prepare-evaluation-plan-disclosure
```

복사 대상은 다음과 같습니다.

```text
~/.claude/skills/prepare-evaluation-plan-disclosure
```

플러그인으로 시험할 때는 저장소의 상위 폴더에서 다음 명령을 실행합니다.

```bash
claude --plugin-dir ./prepare-evaluation-plan-disclosure
```

Claude Code에서는 다음처럼 호출합니다.

```text
/prepare-evaluation-plan-disclosure
```

플러그인 모드에서는 `/prepare-evaluation-plan-disclosure:prepare-evaluation-plan-disclosure`처럼 네임스페이스가 붙을 수 있습니다.

## 개인정보 및 저작권

이 저장소에는 실제 학교 평가계획, 학생 정보 또는 교육기관의 내부 문서가 포함되어 있지 않습니다. 실제 문서를 처리할 때는 소속 기관의 개인정보·문서보안 정책을 확인하세요.

## 라이선스

MIT License
