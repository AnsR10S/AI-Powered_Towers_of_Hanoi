# Towers of Hanoi with AI Solver

A Python implementation of the classic Towers of Hanoi puzzle with:
- Interactive web interface (Flask)
- AI solver using neural networks
- Move prediction and state classification models
- Animated solutions
- Hint system

## Features

- 🎮 **Interactive Gameplay**: Drag-and-drop disks between poles
- 🤖 **AI Integration**: 
  - Neural network for move prediction
  - State classification to detect solved states
- 💡 **Hint System**: Get suggested moves from the AI
- 🚀 **Auto-Solve**: Watch the AI solve the puzzle automatically
- 🎨 **Customizable**: Adjust number of disks (3-8) and visual styles
- 📊 **Training Scripts**: Generate data and train your own models

## Technologies Used

- **Backend**: Python, Flask
- **AI/ML**: TensorFlow/Keras
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Handling**: NumPy, JSON

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AnsR10S/AI-Powered_Towers_of_Hanoi.git
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Train the models (optional - pre-trained models included):
   ```bash
   cd towers_of_hanoi
   python train_simple.py
   ```

## Running the Application

Start the Flask development server:
```bash
cd towers_of_hanoi
python main.py
```

Then open your browser to:
```
http://localhost:5000
```

## Project Structure

```
towers-of-hanoi-ai/
├── core/                      # Core game and AI logic
│   ├── ai_solver.py           # AI solver implementation
│   ├── data_generation.py     # Training data generation
│   ├── game_logic.py          # Game rules and state management
│   └── models/                # Neural network implementations
├── data/                      # Generated data and saved models
├── static/                    # Web assets (CSS, JS)
├── templates/                 # HTML templates
├── config.py                  # Configuration settings
├── train_simple.py            # Model training script
└── main.py                    # Flask application entry point
```

## Configuration

Edit `config.py` to customize:
- Number of disks (3-8)
- Visual styles (colors, sizes)
- AI training parameters
- Animation settings

## Training Your Own Models

1. Generate training data:
   ```python
   from core.data_generation import DataGenerator
   generator = DataGenerator(num_disks=3)
   X_move, y_move = generator.generate_move_data(10000)
   ```

2. Train the models:
   ```bash
   python train_simple.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any:
- Bug fixes
- Feature enhancements
- Documentation improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Classic Towers of Hanoi puzzle
- TensorFlow/Keras for machine learning capabilities
- Flask for web application framework
```
