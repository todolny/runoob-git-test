from flask import Flask, jsonify, render_template
import random
import os
import sys
import re
from flask_cors import CORS


# 获取当前运行的脚本/EXE 的目录
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))



# 获取模板和静态文件夹的绝对路径
template_folder_path = os.path.abspath(os.path.join(base_path, '../templates'))
static_folder_path = os.path.abspath(os.path.join(base_path, '../static'))

# 创建 Flask 实例，明确指定 template_folder 和 static_folder
app = Flask(__name__)  # 但是的但是，要打包后的应用进行识别这里一定不能用template_folder 和 static_folder这样的东西，完全识别不到应有的文件啊！！！！
CORS(app)  # 我是真的服，原来加后面那些参数还会影响运行指定的跨域问题，我就想着自己是已经加了的居然还报错# 允许访问静态文件  # 允许所有跨域请求，或者指定特定的域名

# 获取 .exe 文件所在目录
base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

# 外部 prizes.txt 的路径
external_prizes_file_path = os.path.join(base_path, 'prizes.txt')

# 打包时临时目录内 prizes.txt 的路径
internal_prizes_file_path = os.path.join(getattr(sys, '_MEIPASS', base_path), 'prizes.txt')

# 优先使用外部文件路径
if os.path.exists(external_prizes_file_path):
    prizes_file_path = external_prizes_file_path
    print(f"Using external prizes file at: {prizes_file_path}")
else:
    prizes_file_path = internal_prizes_file_path
    print(f"Using internal prizes file at: {prizes_file_path}")
    print(f"To modify the prize list, please update the file at: {external_prizes_file_path}")

# 从文件加载奖品列表
def load_prizes(file_path):
    """从文件加载奖品列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 使用正则表达式同时匹配英文逗号和中文逗号
            content = file.read()
            return [item.strip() for item in re.split(r'[,\，]', content) if item.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

prizes = load_prizes(prizes_file_path)
print(f"To modify the prize list, please update the file at: {prizes_file_path}")



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
    app.run(debug=True, host='0.0.0.0', port=5000)
