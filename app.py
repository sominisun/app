# from flask import Flask  # 이런 Flask 관련 import 제거
# app = Flask(__name__)   # Flask 앱 초기화 부분 제거

import streamlit as st    # 대신 streamlit 사용
from weather_chatbot import WeatherChatbot

chatbot = WeatherChatbot()

# @app.route('/') 와 같은 데코레이터 제거
# def home():
#     return render_template('home.html')

# Streamlit 스타일
st.title('홈페이지')  # 페이지 제목
st.write('여기에 내용을 작성하세요')

# 다른 Streamlit 컴포넌트 예시
st.header('섹션 제목')
st.text('일반 텍스트')
st.markdown('**마크다운** 지원')

@streamlit.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        data = streamlit.get_json()
        city = data.get('city')
        
        if not city:
            return streamlit.jsonify({
                'success': False,
                'message': '도시 이름을 입력해주세요.'
            }), 400
        
        weather_data = chatbot.get_weather(city)
        
        if weather_data is None:
            return streamlit.jsonify({
                'success': False,
                'message': '날씨 정보를 가져오는데 실패했습니다. 잠시 후 다시 시도해주세요.'
            }), 500
        
        return streamlit.jsonify({
            'success': True,
            'data': weather_data
        })
        
    except Exception as e:
        return streamlit.jsonify({
            'success': False,
            'message': str(e)
        }), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)