# 날씨 AI 에이전트

OpenAI Assistant API와 OpenWeatherMap API를 사용하여 구현한 간단한 날씨 정보 제공 AI 에이전트입니다.

## 기능

- 사용자가 도시 이름을 입력하면 해당 도시의 현재 날씨 정보를 제공합니다.
- 제공되는 날씨 정보:
  - 현재 기온
  - 체감 온도
  - 습도
  - 날씨 상태

## 설치 방법

1. 저장소를 클론합니다:
```bash
git clone <repository-url>
cd <repository-name>
```

2. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
   - `.env.example` 파일을 `.env`로 복사합니다.
   - OpenAI API 키와 OpenWeatherMap API 키를 설정합니다.

## 실행 방법

```bash
python weather_agent.py
```

## API 키 발급 방법

### OpenAI API 키
1. [OpenAI 웹사이트](https://platform.openai.com)에 접속
2. 계정 생성 및 로그인
3. API 키 발급

### OpenWeatherMap API 키
1. [OpenWeatherMap 웹사이트](https://openweathermap.org)에 접속
2. 계정 생성 및 로그인
3. API 키 발급

## 사용 예시

```
날씨 도우미를 시작합니다. '종료'를 입력하면 프로그램이 종료됩니다.
도시 이름을 입력하시면 현재 날씨 정보를 알려드립니다.

질문: 서울 날씨 어때?

도우미: 현재 서울의 날씨 정보입니다:
- 기온: 18.5°C
- 체감온도: 17.8°C
- 습도: 65%
- 날씨 상태: 맑음 