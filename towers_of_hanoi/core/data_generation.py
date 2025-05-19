import numpy as np
from core.game_logic import HanoiGame
from core.ai_solver import HanoiSolver
from config import config
import tensorflow as tf
        
class DataGenerator:
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        
    def generate_move_data(self, num_samples):
        """Generate data without depending on HanoiSolver"""
        X = []
        y = []
        game = HanoiGame(self.num_disks)
        
        # Implement your own move generation logic here
        # For example:
        for _ in range(num_samples):
            # Generate random valid moves
            valid_moves = self._get_valid_moves(game)
            if valid_moves:
                from_pole, to_pole = valid_moves[np.random.randint(len(valid_moves))]
                X.append(self._state_to_array(game.get_state()))
                y.append(from_pole * 3 + to_pole)  # Simple encoding
                game.move_disk(from_pole, to_pole)
        
        return np.array(X), tf.keras.utils.to_categorical(y, num_classes=9)
    
    def generate_state_data(self, num_samples=5000):
        """Generate training data for state classification"""
        X = []
        y = []
        
        # Generate solved states
        game = HanoiGame(self.num_disks)
        for _ in range(num_samples // 2):
            game.reset()
            # Move all disks to target pole
            game.poles = [[], [], list(range(self.num_disks, 0, -1))]
            X.append(self._state_to_array(game.get_state()))
            y.append(1)  # 1 for solved
        
        # Generate random unsolved states
        for _ in range(num_samples // 2):
            game.reset()
            # Make random moves
            for _ in range(np.random.randint(1, 2**self.num_disks - 1)):
                valid_moves = self._get_valid_moves(game)
                if valid_moves:
                    from_pole, to_pole = valid_moves[np.random.randint(len(valid_moves))]
                    game.move_disk(from_pole, to_pole)
            X.append(self._state_to_array(game.get_state()))
            y.append(0)  # 0 for unsolved
        
        return np.array(X), np.array(y)
    
    def _get_valid_moves(self, game):
        """Get all valid moves from current state"""
        valid_moves = []
        for from_pole in range(config.POLE_COUNT):
            for to_pole in range(config.POLE_COUNT):
                if from_pole != to_pole and game.is_valid_move(from_pole, to_pole):
                    valid_moves.append((from_pole, to_pole))
        return valid_moves
    
    def _state_to_array(self, state):
        """Convert game state to numpy array"""
        array = np.zeros((3, self.num_disks))
        for pole_idx, pole in enumerate(state):
            for disk_idx, disk in enumerate(pole):
                array[pole_idx][disk_idx] = disk
        return array
