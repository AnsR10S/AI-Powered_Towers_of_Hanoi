import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout, Input
from tensorflow.keras.optimizers import Adam
from config import config

class StateClassifier:
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        self.model = self._build_model()
        
    def _build_model(self):
        """Build a classifier with proper input layer"""
        model = Sequential([
            Input(shape=(3, self.num_disks)),  # Proper input layer
            Flatten(),
            Dense(64, activation='relu'),
            Dropout(config.AI_DROPOUT_RATE),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(
            optimizer=Adam(learning_rate=config.AI_LEARNING_RATE),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train(self, X_train, y_train, epochs=None, batch_size=None):
        """Train the state classifier"""
        history = self.model.fit(
            X_train, y_train,
            validation_split=config.AI_VALIDATION_SPLIT,
            epochs=epochs or config.AI_EPOCHS,
            batch_size=batch_size or config.AI_BATCH_SIZE
        )
        return history
    
    def is_solved(self, state):
        """Predict if the state is solved"""
        state_array = self._state_to_array(state)
        prediction = self.model.predict(state_array, verbose=0)
        return prediction[0][0] > 0.5
    
    def _state_to_array(self, state):
        """Convert game state to numpy array"""
        array = np.zeros((1, 3, self.num_disks))
        for pole_idx, pole in enumerate(state):
            for disk_idx, disk in enumerate(pole):
                array[0][pole_idx][disk_idx] = disk
        return array
    
    def save_model(self, path=None):
        path = path or config.get_model_path(self.num_disks, "state_classifier")
        self.model.save(path)
    
    def load_model(self, path=None):
        path = path or config.get_model_path(self.num_disks, "state_classifier")
        try:
            self.model = tf.keras.models.load_model(path)
            return True
        except Exception as e:
            print(f"Error loading state classifier: {e}")
            return False
