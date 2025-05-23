let gameState = {
    poles: [[3, 2, 1], [], []],
    numDisks: 3,
    selectedPole: null,
    moves: 0
};

let isSolving = false;
let solutionTimeout = null;

document.addEventListener('DOMContentLoaded', () => {
    initGame();
    
    document.getElementById('new-game').addEventListener('click', newGame);
    document.getElementById('hint').addEventListener('click', getHint);
    document.getElementById('solve').addEventListener('click', solveGame);
    
    document.querySelectorAll('.pole').forEach(pole => {
        pole.addEventListener('click', handlePoleClick);
    });
});

function initGame() {
    renderBoard();
    updateStatus();
}

function renderBoard() {
    document.querySelectorAll('.pole').forEach((poleElement, poleIndex) => {
        // Clear existing disks
        poleElement.innerHTML = '';
        
        // Add disks
        gameState.poles[poleIndex].forEach(diskSize => {
            const disk = document.createElement('div');
            disk.className = 'disk';
            disk.style.width = `${30 + (diskSize * 30)}px`;
            disk.style.backgroundColor = getDiskColor(diskSize, gameState.numDisks);
            disk.dataset.size = diskSize;
            poleElement.appendChild(disk);
        });
    });
}

function handlePoleClick(event) {
    if (isSolving) return; // Don't allow moves while solving
    
    const poleIndex = parseInt(event.currentTarget.dataset.pole);
    
    if (gameState.selectedPole === null) {
        // Select a pole if it has disks
        if (gameState.poles[poleIndex].length > 0) {
            gameState.selectedPole = poleIndex;
            document.querySelector(`.pole[data-pole="${poleIndex}"]`).lastChild.classList.add('selected');
        }
    } else {
        // Try to move disk
        if (gameState.selectedPole !== poleIndex) {
            moveDisk(gameState.selectedPole, poleIndex);
        }
        // Deselect
        document.querySelector(`.pole[data-pole="${gameState.selectedPole}"]`)?.lastChild?.classList.remove('selected');
        gameState.selectedPole = null;
    }
}

function moveDisk(fromPole, toPole) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            from_pole: fromPole,
            to_pole: toPole,
            poles: gameState.poles,
            num_disks: gameState.numDisks
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            gameState.poles = data.poles;
            gameState.moves++;
            renderBoard();
            updateStatus();
            
            if (data.is_solved) {
                alert(`Congratulations! You solved it in ${gameState.moves} moves!`);
                if (isSolving) {
                    stopSolving();
                }
            }
        } else {
            document.getElementById('message').textContent = 'Invalid move!';
            setTimeout(() => {
                document.getElementById('message').textContent = '';
            }, 2000);
        }
    });
}

function newGame() {
    if (isSolving) {
        stopSolving();
    }
    
    const numDisks = parseInt(document.getElementById('disk-count').value);
    
    fetch('/new_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            disks: numDisks
        })
    })
    .then(response => response.json())
    .then(data => {
        gameState.poles = data.poles;
        gameState.numDisks = data.num_disks;
        gameState.moves = 0;
        renderBoard();
        updateStatus();
    });
}

function getHint() {
    if (isSolving) return;
    
    fetch('/hint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            poles: gameState.poles,
            num_disks: gameState.numDisks
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.move) {
            const [fromPole, toPole] = data.move;
            document.getElementById('message').textContent = 
                `Suggested move: Pole ${fromPole + 1} to Pole ${toPole + 1}`;
        } else {
            document.getElementById('message').textContent = 'No hint available';
        }
    });
}

function solveGame() {
    if (isSolving) {
        stopSolving();
        return;
    }
    
    isSolving = true;
    document.getElementById('solve').textContent = 'Stop';
    
    fetch('/solve', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            poles: gameState.poles,
            num_disks: gameState.numDisks
        })
    })
    .then(response => response.json())
    .then(data => {
        animateSolution(data.solution);
    });
}

function stopSolving() {
    isSolving = false;
    clearTimeout(solutionTimeout);
    document.getElementById('solve').textContent = 'Solve';
}

function animateSolution(solution) {
    if (!isSolving || solution.length === 0) {
        stopSolving();
        return;
    }
    
    const [fromPole, toPole] = solution[0];
    moveDisk(fromPole, toPole);
    
    solutionTimeout = setTimeout(() => {
        animateSolution(solution.slice(1));
    }, 1000);
}

function updateStatus() {
    document.getElementById('move-count').textContent = gameState.moves;
}

function getDiskColor(diskSize, totalDisks) {
    const colors = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', 
        '#FF00FF', '#00FFFF', '#FFA500', '#800080'
    ];
    const index = Math.floor((diskSize / totalDisks) * (colors.length - 1));
    return colors[index];
}
