from collections import deque
from config import config

class HanoiGame:
    def __init__(self, num_disks=config.DEFAULT_DISKS):
        if not config.validate_disk_count(num_disks):
            num_disks = max(config.MIN_DISKS, min(num_disks, config.MAX_DISKS))
        self.num_disks = num_disks
        self.reset()
        
    def reset(self):
        """Reset the game with largest disk at bottom"""
        self.poles = [[i for i in range(self.num_disks, 0, -1)], [], []]
        self.moves = 0
        self.history = deque(maxlen=100)

    def is_valid_move(self, from_pole, to_pole):
        """Check if a move is valid"""
        if from_pole not in range(config.POLE_COUNT) or to_pole not in range(config.POLE_COUNT):
            return False
        if from_pole == to_pole:
            return False
        if not self.poles[from_pole]:
            return False
        if not self.poles[to_pole]:
            return True
        return self.poles[from_pole][-1] < self.poles[to_pole][-1]
    
    def move_disk(self, from_pole, to_pole):
        """Move a disk from one pole to another"""
        if self.is_valid_move(from_pole, to_pole):
            disk = self.poles[from_pole].pop()
            self.poles[to_pole].append(disk)
            self.moves += 1
            self.history.append((from_pole, to_pole))
            return True
        return False
    
    def undo_move(self):
        """Undo the last move"""
        if self.history:
            to_pole, from_pole = self.history.pop()  # Reverse the move
            disk = self.poles[from_pole].pop()
            self.poles[to_pole].append(disk)
            self.moves -= 1
            return True
        return False
    
    def is_solved(self):
        """Check if the puzzle is solved"""
        return len(self.poles[-1]) == self.num_disks
    
    def get_state(self):
        """Returns a hashable representation of the current state"""
        return tuple(tuple(pole) for pole in self.poles)
    
    def get_progress(self):
        """Returns completion percentage (0-100)"""
        return (len(self.poles[-1]) / self.num_disks) * 100
    
    def get_legal_moves(self):
        """Returns list of all legal moves from current state"""
        moves = []
        for from_pole in range(config.POLE_COUNT):
            for to_pole in range(config.POLE_COUNT):
                if self.is_valid_move(from_pole, to_pole):
                    moves.append((from_pole, to_pole))
        return moves
