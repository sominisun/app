import random
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, List, Tuple

def validate_city(city: str) -> bool:
    """
    도시 이름의 유효성을 검사합니다.
    
    Args:
        city (str): 검사할 도시 이름
    
    Returns:
        bool: 도시 이름 유효성 여부
    """
    if not city or not isinstance(city, str):
        logging.error('유효하지 않은 도시 이름')
        return False
    return True

def get_season_info(month: int) -> Tuple[str, Tuple[float, float]]:
    """
    월별 계절 정보를 반환합니다.
    
    Args:
        month (int): 월 (1-12)
    
    Returns:
        Tuple[str, Tuple[float, float]]: (계절, 온도 범위)
    """
    if 3 <= month <= 5:
        return "봄", (10, 25)
    elif 6 <= month <= 8:
        return "여름", (25, 35)
    elif 9 <= month <= 11:
        return "가을", (10, 25)
    else:
        return "겨울", (-5, 10)

def generate_hourly_forecast(now: datetime, current_temp: float, weather_states: List[str]) -> List[Dict[str, Any]]:
    """
    시간별 예보를 생성합니다.
    
    Args:
        now (datetime): 현재 시간
        current_temp (float): 현재 기온
        weather_states (List[str]): 가능한 날씨 상태 목록
    
    Returns:
        List[Dict[str, Any]]: 시간별 예보 목록
    """
    hourly_forecast = []
    for i in range(24):
        forecast_time = now + timedelta(hours=i)
        temp = round(current_temp + random.uniform(-5, 5), 1)
        weather = random.choice(weather_states)
        hourly_forecast.append({
            "time": forecast_time.strftime("%H:00"),
            "temp": temp,
            "weather": weather
        })
    return hourly_forecast

def generate_weekly_forecast(now: datetime, temp_range: Tuple[float, float], weather_states: List[str]) -> List[Dict[str, Any]]:
    """
    주간 예보를 생성합니다.
    
    Args:
        now (datetime): 현재 시간
        temp_range (Tuple[float, float]): 온도 범위
        weather_states (List[str]): 가능한 날씨 상태 목록
    
    Returns:
        List[Dict[str, Any]]: 주간 예보 목록
    """
    forecast = []
    for i in range(7):
        date = now + timedelta(days=i)
        temp = round(random.uniform(temp_range[0], temp_range[1]), 1)
        weather = random.choice(weather_states)
        forecast.append({
            "date": date.strftime("%m/%d"),
            "day": ["월", "화", "수", "목", "금", "토", "일"][date.weekday()],
            "temp": temp,
            "weather": weather
        })
    return forecast

def get_current_weather(city: str, country_code: str = "kr") -> Dict[str, Any]:
    """
    도시별 날씨 정보를 시뮬레이션하여 제공합니다.
    
    Args:
        city (str): 도시 이름
        country_code (str): 국가 코드 (기본값: kr)
    
    Returns:
        Dict[str, Any]: 날씨 정보 딕셔너리
    """
    try:
        # 도시 이름 검증
        if not validate_city(city):
            raise ValueError("유효하지 않은 도시 이름입니다.")
        
        logging.info(f'날씨 정보 생성 시작: {city}')
        
        # 현재 시간과 계절 정보
        now = datetime.now()
        month = now.month
        hour = now.hour
        
        # 계절 정보 가져오기
        season, temp_range = get_season_info(month)
        logging.info(f'계절 정보: {season}, 온도 범위: {temp_range}')
        
        # 현재 날씨 상태
        weather_states = ["맑음", "흐림", "비", "눈", "안개", "천둥번개", "미세먼지"]
        current_weather = random.choice(weather_states)
        
        # 현재 기온 (계절에 맞는 범위 내에서)
        current_temp = round(random.uniform(temp_range[0], temp_range[1]), 1)
        
        # 체감온도 (현재 기온과 ±2도 차이)
        feels_like = round(current_temp + random.uniform(-2, 2), 1)
        
        # 습도 (30-90% 범위)
        humidity = random.randint(30, 90)
        
        # 풍속 (0-15 m/s 범위)
        wind_speed = round(random.uniform(0, 15), 1)
        
        # 미세먼지 상태
        air_quality_states = ["좋음", "보통", "나쁨", "매우 나쁨"]
        air_quality = random.choice(air_quality_states)
        
        # 시간별 예보 생성
        hourly_forecast = generate_hourly_forecast(now, current_temp, weather_states)
        logging.info('시간별 예보 생성 완료')
        
        # 주간 예보 생성
        forecast = generate_weekly_forecast(now, temp_range, weather_states)
        logging.info('주간 예보 생성 완료')
        
        weather_data = {
            "city": city,
            "season": season,
            "current": {
                "temperature": current_temp,
                "feels_like": feels_like,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "weather": current_weather,
                "air_quality": air_quality
            },
            "hourly": hourly_forecast,
            "forecast": forecast
        }
        
        logging.info(f'날씨 정보 생성 완료: {city}')
        return weather_data
        
    except Exception as e:
        logging.error(f'날씨 정보 생성 중 오류 발생: {str(e)}')
        raise 