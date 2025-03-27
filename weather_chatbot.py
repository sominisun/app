import os
import logging
import requests
from dotenv import load_dotenv

class WeatherChatbot:
    def __init__(self):
        load_dotenv()
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.openweather_api_key:
            raise ValueError("OPENWEATHER_API_KEY가 설정되지 않았습니다.")

    def get_weather(self, city):
        """도시 이름으로 날씨 정보를 가져옵니다."""
        try:
            # 한글 도시/지역 이름을 영어로 변환
            city_mapping = {
                # 서울 지역
                '서울': 'Seoul',
                '강남구': 'Gangnam-gu, Seoul',
                '서초구': 'Seocho-gu, Seoul',
                '송파구': 'Songpa-gu, Seoul',
                '강서구': 'Gangseo-gu, Seoul',
                '마포구': 'Mapo-gu, Seoul',
                '용산구': 'Yongsan-gu, Seoul',
                '영등포구': 'Yeongdeungpo-gu, Seoul',
                '종로구': 'Jongno-gu, Seoul',
                '중구': 'Jung-gu, Seoul',
                '성동구': 'Seongdong-gu, Seoul',
                '광진구': 'Gwangjin-gu, Seoul',
                '동대문구': 'Dongdaemun-gu, Seoul',
                '중랑구': 'Jungnang-gu, Seoul',
                '성북구': 'Seongbuk-gu, Seoul',
                '강북구': 'Gangbuk-gu, Seoul',
                '도봉구': 'Dobong-gu, Seoul',
                '노원구': 'Nowon-gu, Seoul',
                '은평구': 'Eunpyeong-gu, Seoul',
                '서대문구': 'Seodaemun-gu, Seoul',
                '양천구': 'Yangcheon-gu, Seoul',
                '구로구': 'Guro-gu, Seoul',
                '금천구': 'Geumcheon-gu, Seoul',
                '동작구': 'Dongjak-gu, Seoul',
                '관악구': 'Gwanak-gu, Seoul',
                '강동구': 'Gangdong-gu, Seoul',

                # 부산 지역
                '부산': 'Busan',
                '중구': 'Jung-gu, Busan',
                '서구': 'Seo-gu, Busan',
                '동구': 'Dong-gu, Busan',
                '영도구': 'Yeongdo-gu, Busan',
                '부산진구': 'Busanjin-gu, Busan',
                '동래구': 'Dongnae-gu, Busan',
                '남구': 'Nam-gu, Busan',
                '북구': 'Buk-gu, Busan',
                '해운대구': 'Haeundae-gu, Busan',
                '사하구': 'Saha-gu, Busan',
                '금정구': 'Geumjeong-gu, Busan',
                '강서구': 'Gangseo-gu, Busan',
                '연제구': 'Yeonje-gu, Busan',
                '수영구': 'Suyeong-gu, Busan',
                '사상구': 'Sasang-gu, Busan',
                '기장군': 'Gijang-gun, Busan',

                # 인천 지역
                '인천': 'Incheon',
                '중구': 'Jung-gu, Incheon',
                '동구': 'Dong-gu, Incheon',
                '미추홀구': 'Michuhol-gu, Incheon',
                '연수구': 'Yeonsu-gu, Incheon',
                '남동구': 'Namdong-gu, Incheon',
                '부평구': 'Bupyeong-gu, Incheon',
                '계양구': 'Gyeyang-gu, Incheon',
                '서구': 'Seo-gu, Incheon',
                '강화군': 'Ganghwa-gun, Incheon',
                '옹진군': 'Ongjin-gun, Incheon',

                # 기타 주요 도시
                '대구': 'Daegu',
                '대전': 'Daejeon',
                '광주': 'Gwangju',
                '수원': 'Suwon',
                '울산': 'Ulsan',
                '창원': 'Changwon',
                '고양': 'Goyang',
                '용인': 'Yongin',
                '성남': 'Seongnam',
                '제주': 'Jeju',
                '청주': 'Cheongju',
                '안산': 'Ansan',
                '전주': 'Jeonju',
                '천안': 'Cheonan',
                '안양': 'Anyang',
                '남양주': 'Namyangju',
                '김해': 'Gimhae'
            }

            # 입력된 지역명에서 공백 제거
            city = city.strip()
            
            # 지역명이 "구" 또는 "동"으로 끝나는 경우, 도시 이름을 추가
            if city.endswith(('구', '동', '읍', '면')):
                # 서울의 구/동인 경우
                if any(district in city for district in ['강남', '서초', '송파', '마포', '용산', '영등포', '종로']):
                    english_city = f"{city_mapping.get(city, city)}, Seoul"
                # 부산의 구/동인 경우
                elif any(district in city for district in ['해운대', '부산진', '동래', '사하', '금정']):
                    english_city = f"{city_mapping.get(city, city)}, Busan"
                # 인천의 구/동인 경우
                elif any(district in city for district in ['미추홀', '연수', '남동', '부평', '계양']):
                    english_city = f"{city_mapping.get(city, city)}, Incheon"
                else:
                    english_city = city_mapping.get(city, city)
            else:
                english_city = city_mapping.get(city, city)

            # 현재 날씨 정보 가져오기
            current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={english_city}&appid={self.openweather_api_key}&units=metric&lang=kr"
            current_response = requests.get(current_weather_url)
            
            if current_response.status_code != 200:
                logging.error(f"날씨 정보 가져오기 실패: {current_response.status_code}")
                return None
            
            current_data = current_response.json()
            lat, lon = current_data['coord']['lat'], current_data['coord']['lon']
            
            # 시간별/주간 예보 및 대기질 정보 가져오기
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.openweather_api_key}&units=metric&lang=kr"
            air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.openweather_api_key}"
            
            forecast_response = requests.get(forecast_url)
            air_quality_response = requests.get(air_quality_url)
            
            if forecast_response.status_code != 200 or air_quality_response.status_code != 200:
                logging.error("예보 또는 대기질 정보 가져오기 실패")
                return None
            
            forecast_data = forecast_response.json()
            air_quality_data = air_quality_response.json()
            
            # 현재 날씨 정보
            current = {
                'temperature': round(current_data['main']['temp']),
                'feels_like': round(current_data['main']['feels_like']),
                'humidity': current_data['main']['humidity'],
                'wind_speed': round(current_data['wind']['speed'], 1),
                'weather': current_data['weather'][0]['description']
            }
            
            # 시간별 예보 (다음 24시간)
            hourly = []
            for item in forecast_data['list'][:8]:
                hourly.append({
                    'time': item['dt_txt'].split(' ')[1][:5],
                    'temp': round(item['main']['temp']),
                    'weather': item['weather'][0]['description']
                })
            
            # 주간 예보
            forecast = []
            daily_forecasts = {}
            
            # 현재 날짜로부터 가장 가까운 월요일을 찾습니다
            from datetime import datetime, timedelta
            current_date = datetime.now()
            days_until_monday = (0 - current_date.weekday()) % 7
            next_monday = current_date + timedelta(days=days_until_monday)
            
            # 월요일부터 일요일까지 7일의 데이터 생성
            for i in range(7):
                date = (next_monday + timedelta(days=i)).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'temps': [20],
                        'weather': '맑음'
                    }
            
            # OpenWeather API에서 받은 예보 데이터로 업데이트
            for item in forecast_data['list']:
                date = item['dt_txt'].split(' ')[0]
                if date in daily_forecasts:
                    daily_forecasts[date]['temps'].append(item['main']['temp'])
                    daily_forecasts[date]['weather'] = item['weather'][0]['description']

            # 7일 전체 예보 생성 (월요일부터 일요일 순서로)
            for date, data in sorted(daily_forecasts.items())[:7]:
                avg_temp = round(sum(data['temps']) / len(data['temps']))
                day_name = self._get_day_name(date)
                forecast.append({
                    'day': day_name,
                    'temp': avg_temp,
                    'weather': data['weather']
                })
            
            # 대기질 정보
            air_quality_details = {
                'pm10': air_quality_data['list'][0]['components']['pm10'],
                'pm25': air_quality_data['list'][0]['components']['pm2_5']
            }
            
            return {
                'success': True,
                'city': city,
                'current': current,
                'hourly': hourly,
                'forecast': forecast,
                'air_quality_details': air_quality_details
            }
            
        except Exception as e:
            logging.error(f"날씨 정보 처리 중 오류 발생: {str(e)}")
            return None

    def _get_day_name(self, date_str):
        """날짜 문자열을 요일 이름으로 변환합니다."""
        from datetime import datetime
        days = {
            0: '월',
            1: '화',
            2: '수',
            3: '목',
            4: '금',
            5: '토',
            6: '일'
        }
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return days[date_obj.weekday()] 