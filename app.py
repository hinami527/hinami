from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 初期設定
point_settings = {
    "kill_point": 1,  # キルポイントのデフォルト値
    "rank_points": [],  # 順位ポイント
    "kill_limit": 0,    # キルポイント制限
    "team_count": 0     # チーム数
}

teams = []

@app.route('/')
def index():
    return render_template('index.html', teams=teams, point_settings=point_settings)

@app.route('/settings', methods=['POST'])
def set_settings():
    point_settings['team_count'] = int(request.form['team_count'])
    point_settings['kill_point'] = int(request.form['kill_point'])
    point_settings['kill_limit'] = int(request.form['kill_limit'])
    point_settings['rank_points'] = [int(request.form[f'rank_point_{i+1}']) for i in range(point_settings['team_count'])]
    return redirect(url_for('index'))

@app.route('/add_team', methods=['POST'])
def add_team():
    team_name = request.form['team_name']
    kills = int(request.form['kills'])
    rank = int(request.form['rank'])
    
    if kills > point_settings['kill_limit']:
        return redirect(url_for('index'))  # キル制限を超えていた場合はリダイレクト
    
    points = calculate_points(kills, rank)
    teams.append({'name': team_name, 'kills': kills, 'rank': rank, 'points': points})
    return redirect(url_for('index'))

def calculate_points(kills, rank):
    kill_points = kills * point_settings['kill_point']
    rank_points = point_settings['rank_points'][rank - 1] if rank <= len(point_settings['rank_points']) else 0
    return kill_points + rank_points

if __name__ == '__main__':
    app.run(debug=True)