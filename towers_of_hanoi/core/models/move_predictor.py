import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from config import config

class MovePredictor:
    def __init__(self, num_disks=3):
        self.num_disks = num_disks
        self.model = self._build_model()

    def _build_model(self):
        """Build a neural network to predict next moves"""
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(3, self.num_disks)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(9, activation='softmax')
        ])
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train(self, X_train, y_train, epochs=None, batch_size=None):
        """Train the move prediction model"""
        checkpoint = ModelCheckpoint(
            config.get_model_path(self.num_disks, "move_predictor"),
            monitor='val_accuracy',
            save_best_only=True,
            mode='max'
        )
        
        history = self.model.fit(
            X_train, y_train,
            validation_split=config.AI_VALIDATION_SPLIT,
            epochs=epochs or config.AI_EPOCHS,
            batch_size=batch_size or config.AI_BATCH_SIZE,
            callbacks=[checkpoint]
        )
        return history
    
    def predict_move(self, state):
        """Predict the best next move from current state"""
        state_array = self._state_to_array(state)
        predictions = self.model.predict(state_array, verbose=0)
        move = np.argmax(predictions[0])
        from_pole = move // 3
        to_pole = move % 3
        return from_pole, to_pole
    
    def _state_to_array(self, state):
        """Convert game state to numpy array for model input"""
        array = np.zeros((1, 3, self.num_disks))
        for pole_idx, pole in enumerate(state):
            for disk_idx, disk in enumerate(pole):
                array[0][pole_idx][disk_idx] = disk
        return array
    
    def save_model(self, path=None):
        path = path or config.get_model_path(self.num_disks, "move_predictor")
        self.model.save(path)
    
    def load_model(self, path=None):
        path = path or config.get_model_path(self.num_disks, "move_predictor")
        try:
            self.model = tf.keras.models.load_model(path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
