import numpy as np
from .models.move_predictor import MovePredictor
from .models.state_classifier import StateClassifier
from config import config

class HanoiSolver:
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        self.move_predictor = MovePredictor(num_disks)
        self.state_classifier = StateClassifier(num_disks)
        self.models_loaded = self.load_models()
        
    def load_models(self):
        """Attempt to load pre-trained models"""
        try:
            move_loaded = self.move_predictor.load_model()
            state_loaded = self.state_classifier.load_model()
            return move_loaded and state_loaded
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    def solve_iterative(self, game):
        """Non-recursive solution that works with animation"""
        n = game.num_disks
        moves = []
        
        def _move_disks(n, source, target, auxiliary):
            if n > 0:
                _move_disks(n-1, source, auxiliary, target)
                moves.append((source, target))
                _move_disks(n-1, auxiliary, target, source)
                
        _move_disks(n, 0, 2, 1)
        return moves
    
    def solve_with_ai(self, game, max_moves=100):
        if not self.models_loaded:
            return self.solve_iterative(game)

        moves = []
        for _ in range(max_moves):
            if game.is_solved():
                break

            from_pole, to_pole = self.move_predictor.predict_move(game.get_state())
            if game.is_valid_move(from_pole, to_pole):
                game.move_disk(from_pole, to_pole)
                moves.append((from_pole, to_pole))
            else:
                return self.solve_iterative(game)
        return moves
    
    def suggest_move(self, game_state):
        """Improved move suggestion"""
        if not self.models_loaded:
            # Fallback to simple rule: move smallest disk
            for from_pole in range(3):
                if game_state[from_pole] and min(game_state[from_pole]) == 1:
                    # Try to move to non-original pole
                    for to_pole in [1, 2, 0]:
                        if from_pole != to_pole and (not game_state[to_pole] or game_state[to_pole][-1] > 1):
                            return (from_pole, to_pole)
            return None
        
        return self.move_predictor.predict_move(game_state)

    def is_state_solved(self, game_state):
        if not self.models_loaded:
            return len(game_state[-1]) == self.num_disks
        return self.state_classifier.is_solved(game_state)
