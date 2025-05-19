import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from core.data_generation import DataGenerator
from core.models.move_predictor import MovePredictor
from core.models.state_classifier import StateClassifier
from config import config

def train_simple_models(num_disks=3):
    print(f"Training models for {num_disks} disks...")
    
    # Ensure directories exist
    os.makedirs(config.get_model_dir(), exist_ok=True)
    
    # Generate data
    generator = DataGenerator(num_disks)
    
    # Train move predictor
    print("\nTraining move predictor...")
    X_move, y_move = generator.generate_move_data(1000)  # More data
    move_model = MovePredictor(num_disks)
    history = move_model.model.fit(
        X_move, y_move,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    move_model.save_model()
    print(f"Move predictor trained - final accuracy: {history.history['accuracy'][-1]:.2f}")
    
    # Train state classifier
    print("\nTraining state classifier...")
    X_state, y_state = generator.generate_state_data(500)
    state_model = StateClassifier(num_disks)
    history = state_model.model.fit(
        X_state, y_state,
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    state_model.save_model()
    print(f"State classifier trained - final accuracy: {history.history['accuracy'][-1]:.2f}")
    
    print(f"\nModels saved to {config.get_model_dir()}")

if __name__ == "__main__":
    for disks in range(3, 9):  # Train models for 3-8 disks
        train_simple_models(disks)
