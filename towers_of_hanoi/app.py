from flask import Flask, render_template, request, jsonify
from core.game_logic import HanoiGame
from core.ai_solver import HanoiSolver
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    num_disks = int(request.json.get('disks', 3))
    game = HanoiGame(num_disks)
    solver = HanoiSolver(num_disks)
    return jsonify({
        'poles': game.poles,
        'num_disks': num_disks
    })

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    from_pole = data['from_pole']
    to_pole = data['to_pole']
    
    game = HanoiGame(data['num_disks'])
    game.poles = data['poles']
    
    if game.move_disk(from_pole, to_pole):
        return jsonify({
            'success': True,
            'poles': game.poles,
            'is_solved': game.is_solved()
        })
    return jsonify({'success': False})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    game = HanoiGame(data['num_disks'])
    game.poles = data['poles']
    solver = HanoiSolver(data['num_disks'])
    solution = solver.solve_iterative(game)
    return jsonify({'solution': solution})

@app.route('/hint', methods=['POST'])
def hint():
    data = request.json
    game = HanoiGame(data['num_disks'])
    game.poles = data['poles']
    solver = HanoiSolver(data['num_disks'])
    move = solver.suggest_move(game.poles)
    
    if move:
        # Convert numpy.int64 to regular Python int
        move = [int(move[0]), int(move[1])]
    
    return jsonify({'move': move})

if __name__ == '__main__':
    app.run(debug=True)
