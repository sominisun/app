from flask import Flask, request, jsonify, render_template
from weather_chatbot import WeatherChatbot

app = Flask(__name__)
chatbot = WeatherChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city = data.get('city')
        
        if not city:
            return jsonify({
                'success': False,
                'message': '도시 이름을 입력해주세요.'
            }), 400
        
        weather_data = chatbot.get_weather(city)
        
        if weather_data is None:
            return jsonify({
                'success': False,
                'message': '날씨 정보를 가져오는데 실패했습니다. 잠시 후 다시 시도해주세요.'
            }), 500
        
        return jsonify({
            'success': True,
            'data': weather_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 