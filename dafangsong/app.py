from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# 预设奖品列表
prizes = [
    "iPhone 15",
    "MacBook Pro",
    "AirPods Pro",
    "500元购物卡",
    "Kindle电子书",
    "Switch游戏机",
    "谢谢参与"
]

@app.route('/')
def index():
    # 渲染前端页面
    return render_template('index.html')

@app.route('/draw', methods=['GET'])
def draw_prize():
    # 随机抽奖
    selected_prize = random.choice(prizes)
    return jsonify({'selected_prize': selected_prize})

if __name__ == '__main__':
    app.run(debug=True)
