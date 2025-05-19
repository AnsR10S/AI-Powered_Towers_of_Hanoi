import os
import json
from pathlib import Path
from typing import List, Dict, Union, Tuple

class Config:
    """Central configuration class for Towers of Hanoi game with enhanced features"""
    
    # Game settings
    MIN_DISKS: int = 3
    MAX_DISKS: int = 8
    DEFAULT_DISKS: int = 3
    MIN_MOVES_CACHE: Dict[int, int] = {  # Minimum moves required for n disks
        3: 7,
        4: 15,
        5: 31,
        6: 63,
        7: 127,
        8: 255
    }
    
    # GUI settings
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    POLE_COUNT: int = 3
    POLE_COLORS: List[str] = ["#8B4513", "#8B4513", "#8B4513"]  # Brown
    DISK_COLORS: List[str] = [
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
        "#FFFF00",  # Yellow
        "#FF00FF",  # Magenta
        "#00FFFF",  # Cyan
        "#FFA500",  # Orange
        "#800080"   # Purple
    ]
    BACKGROUND_COLOR: str = "#F5F5DC"  # Beige
    HIGHLIGHT_COLOR: str = "#FFFF00"  # Yellow
    SUGGEST_COLOR: str = "#00FFFF"    # Cyan
    TEXT_COLOR: str = "#000000"       # Black
    DISABLED_COLOR: str = "#AAAAAA"   # Gray
    
    # Animation settings
    MOVE_ANIMATION_DURATION: int = 500  # ms
    SOLUTION_DELAY: int = 1000  # ms between moves in auto-solve
    ANIMATION_EASING: str = "InOutQuad"  # PyQt easing curve
    DISK_HEIGHT: int = 20  # px
    DISK_MIN_WIDTH: int = 30  # px
    DISK_MAX_WIDTH: int = 200  # px
    
    # AI settings
    AI_MODEL_DIR: str = "data/models"
    MOVE_PREDICTOR_FILE: str = "move_predictor_{disks}d.h5"
    STATE_CLASSIFIER_FILE: str = "state_classifier_{disks}d.h5"
    AI_TRAINING_SAMPLES: int = 10000
    AI_VALIDATION_SPLIT: float = 0.2
    AI_EPOCHS: int = 20
    AI_BATCH_SIZE: int = 32
    AI_LEARNING_RATE: float = 0.001
    AI_DROPOUT_RATE: float = 0.2
    
    # Sound settings
    SOUND_ENABLED: bool = True
    MOVE_SOUND_FILE: str = "sounds/move.wav"
    VICTORY_SOUND_FILE: str = "sounds/victory.wav"
    
    @staticmethod
    def get_base_dir() -> Path:
        """Get the base directory of the project"""
        return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    @staticmethod
    def get_data_dir() -> Path:
        """Get the data directory path"""
        data_dir = Config.get_base_dir() / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    @staticmethod
    def get_model_dir() -> Path:
        """Get the model directory path"""
        model_dir = Config.get_base_dir() / Config.AI_MODEL_DIR
        model_dir.mkdir(parents=True, exist_ok=True)
        return model_dir
    
    @staticmethod
    def get_sound_dir() -> Path:
        """Get the sound directory path"""
        sound_dir = Config.get_base_dir() / "sounds"
        sound_dir.mkdir(parents=True, exist_ok=True)
        return sound_dir
    
    @staticmethod
    def get_model_path(disks: int, model_type: str = "move_predictor") -> Path:
        """Get path to trained model file with validation"""
        if not Config.validate_disk_count(disks):
            raise ValueError(f"Invalid disk count: {disks}")
            
        model_dir = Config.get_model_dir()
        
        if model_type == "move_predictor":
            filename = Config.MOVE_PREDICTOR_FILE.format(disks=disks)
        elif model_type == "state_classifier":
            filename = Config.STATE_CLASSIFIER_FILE.format(disks=disks)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return model_dir / filename
    
    @staticmethod
    def get_sound_path(sound_type: str) -> Path:
        """Get path to sound file"""
        sound_dir = Config.get_sound_dir()
        
        if sound_type == "move":
            return sound_dir / Config.MOVE_SOUND_FILE.split('/')[-1]
        elif sound_type == "victory":
            return sound_dir / Config.VICTORY_SOUND_FILE.split('/')[-1]
        else:
            raise ValueError(f"Unknown sound type: {sound_type}")
    
    @staticmethod
    def save_user_settings(settings: Dict[str, Union[int, bool, str]]) -> None:
        """Save user settings to JSON file"""
        settings_path = Config.get_data_dir() / "user_settings.json"
        with open(settings_path, 'w') as f:
            json.dump(settings, f, indent=4)
    
    @staticmethod
    def load_user_settings() -> Dict[str, Union[int, bool, str]]:
        """Load user settings from JSON file"""
        settings_path = Config.get_data_dir() / "user_settings.json"
        default_settings = Config.get_default_game_config()
        
        try:
            with open(settings_path, 'r') as f:
                user_settings = json.load(f)
                # Validate loaded settings
                return {**default_settings, **user_settings}
        except (FileNotFoundError, json.JSONDecodeError):
            return default_settings
    
    @staticmethod
    def get_default_game_config() -> Dict[str, Union[int, bool, str]]:
        """Get default game configuration"""
        return {
            "disks": Config.DEFAULT_DISKS,
            "animation_enabled": True,
            "ai_assistance": True,
            "show_tooltips": True,
            "sound_enabled": Config.SOUND_ENABLED,
            "theme": "default"
        }
    
    @staticmethod
    def validate_disk_count(disks: int) -> bool:
        """Validate number of disks is within allowed range"""
        return Config.MIN_DISKS <= disks <= Config.MAX_DISKS
    
    @staticmethod
    def get_min_moves(disks: int) -> int:
        """Get minimum moves required to solve for n disks"""
        return Config.MIN_MOVES_CACHE.get(disks, (2 ** disks) - 1)
    
    @staticmethod
    def get_disk_color(disk_size: int, total_disks: int) -> str:
        """Get color for a disk based on its size and total disks"""
        if not Config.validate_disk_count(total_disks):
            total_disks = max(Config.MIN_DISKS, min(total_disks, Config.MAX_DISKS))
        
        if disk_size < 1 or disk_size > total_disks:
            disk_size = max(1, min(disk_size, total_disks))
        
        normalized = int((disk_size / total_disks) * (len(Config.DISK_COLORS) - 1))
        return Config.DISK_COLORS[normalized]

    @staticmethod
    def get_disk_width(disk_size: int, total_disks: int) -> int:
        """Calculate disk width based on its size"""
        return Config.DISK_MIN_WIDTH + int(
            (Config.DISK_MAX_WIDTH - Config.DISK_MIN_WIDTH) * 
            (disk_size / total_disks)
        )

# Singleton configuration instance
config = Config()
