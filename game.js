// 3D Garage Parking Game
let scene, camera, renderer;
let player, ground;
let garages = [];
let obstacles = [];
let score = 0;
let time = 0;
let gameActive = true;
let highScore = 0;
let parksCount = 0;

// Game settings
const PLAYER_SPEED = 0.15;
const GAME_WIDTH = 20;
const GAME_DEPTH = 30;
const SPAWN_DISTANCE = 25;
const GARAGE_SPAWN_RATE = 0.02;
const OBSTACLE_SPAWN_RATE = 0.03;

// Input
const keys = {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false
};

// Initialize the game
function init() {
    // Load high score
    highScore = parseInt(localStorage.getItem('garageGameHighScore') || '0');
    document.getElementById('high-score').textContent = highScore;

    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87ceeb);
    scene.fog = new THREE.Fog(0x87ceeb, 10, 50);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 8, 5);
    camera.lookAt(0, 0, -5);

    // Renderer setup
    const canvas = document.getElementById('canvas');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.left = -30;
    directionalLight.shadow.camera.right = 30;
    directionalLight.shadow.camera.top = 30;
    directionalLight.shadow.camera.bottom = -30;
    scene.add(directionalLight);

    // Ground
    const groundGeometry = new THREE.PlaneGeometry(GAME_WIDTH, 100);
    const groundMaterial = new THREE.MeshStandardMaterial({
        color: 0x444444,
        roughness: 0.8
    });
    ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Road markings
    for (let i = -50; i < 50; i += 4) {
        const lineGeometry = new THREE.BoxGeometry(0.3, 0.05, 2);
        const lineMaterial = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        const line = new THREE.Mesh(lineGeometry, lineMaterial);
        line.position.set(0, 0.05, i);
        scene.add(line);
    }

    // Player (car)
    createPlayer();

    // Event listeners
    window.addEventListener('keydown', (e) => {
        if (keys.hasOwnProperty(e.key)) {
            keys[e.key] = true;
            e.preventDefault();
        }
    });

    window.addEventListener('keyup', (e) => {
        if (keys.hasOwnProperty(e.key)) {
            keys[e.key] = false;
            e.preventDefault();
        }
    });

    window.addEventListener('resize', onWindowResize);

    document.getElementById('restart-btn').addEventListener('click', restartGame);

    // Start game loop
    animate();
    startTimer();
}

function createPlayer() {
    const carGroup = new THREE.Group();

    // Car body
    const bodyGeometry = new THREE.BoxGeometry(1.2, 0.6, 2);
    const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 0.4;
    body.castShadow = true;
    carGroup.add(body);

    // Car roof
    const roofGeometry = new THREE.BoxGeometry(0.9, 0.5, 1.2);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0xcc0000 });
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.y = 0.9;
    roof.position.z = -0.2;
    roof.castShadow = true;
    carGroup.add(roof);

    // Wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.25, 0.25, 0.2, 16);
    const wheelMaterial = new THREE.MeshStandardMaterial({ color: 0x222222 });

    const wheelPositions = [
        [-0.6, 0.25, 0.7],
        [0.6, 0.25, 0.7],
        [-0.6, 0.25, -0.7],
        [0.6, 0.25, -0.7]
    ];

    wheelPositions.forEach(pos => {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(...pos);
        wheel.castShadow = true;
        carGroup.add(wheel);
    });

    carGroup.position.set(0, 0, 0);
    player = carGroup;
    scene.add(player);
}

function createGarage(x, z) {
    const garageGroup = new THREE.Group();

    // Garage structure
    const wallMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });

    // Back wall
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(3, 2.5, 0.2), wallMaterial);
    backWall.position.z = -1.4;
    backWall.castShadow = true;
    garageGroup.add(backWall);

    // Left wall
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.5, 3), wallMaterial);
    leftWall.position.x = -1.4;
    leftWall.castShadow = true;
    garageGroup.add(leftWall);

    // Right wall
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.5, 3), wallMaterial);
    rightWall.position.x = 1.4;
    rightWall.castShadow = true;
    garageGroup.add(rightWall);

    // Roof
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0x654321 });
    const roof = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.2, 3.2), roofMaterial);
    roof.position.y = 1.3;
    roof.castShadow = true;
    garageGroup.add(roof);

    // Door frame (front opening)
    const doorFrameTop = new THREE.Mesh(new THREE.BoxGeometry(3, 0.3, 0.2), wallMaterial);
    doorFrameTop.position.set(0, 1.1, 1.4);
    doorFrameTop.castShadow = true;
    garageGroup.add(doorFrameTop);

    // Parking indicator (glowing green)
    const indicatorGeometry = new THREE.BoxGeometry(0.4, 0.4, 0.1);
    const indicatorMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const indicator = new THREE.Mesh(indicatorGeometry, indicatorMaterial);
    indicator.position.set(0, 2, -1.3);
    garageGroup.add(indicator);

    garageGroup.position.set(x, 1.25, z);
    garageGroup.userData.isGarage = true;

    scene.add(garageGroup);
    garages.push(garageGroup);
}

function createObstacle(x, z) {
    const obstacleGroup = new THREE.Group();

    // Random obstacle type
    const type = Math.random();

    if (type < 0.5) {
        // Cone
        const coneGeometry = new THREE.ConeGeometry(0.4, 1.2, 8);
        const coneMaterial = new THREE.MeshStandardMaterial({ color: 0xff6600 });
        const cone = new THREE.Mesh(coneGeometry, coneMaterial);
        cone.position.y = 0.6;
        cone.castShadow = true;
        obstacleGroup.add(cone);

        // White stripe
        const stripeGeometry = new THREE.CylinderGeometry(0.42, 0.42, 0.3, 8);
        const stripeMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
        const stripe = new THREE.Mesh(stripeGeometry, stripeMaterial);
        stripe.position.y = 0.6;
        obstacleGroup.add(stripe);
    } else {
        // Barrier
        const barrierGeometry = new THREE.BoxGeometry(2, 0.3, 0.3);
        const barrierMaterial = new THREE.MeshStandardMaterial({
            color: 0xff0000,
            emissive: 0x440000
        });
        const barrier = new THREE.Mesh(barrierGeometry, barrierMaterial);
        barrier.position.y = 0.5;
        barrier.castShadow = true;
        obstacleGroup.add(barrier);

        // Posts
        const postGeometry = new THREE.CylinderGeometry(0.1, 0.1, 1, 8);
        const postMaterial = new THREE.MeshStandardMaterial({ color: 0x333333 });

        [-0.9, 0.9].forEach(xPos => {
            const post = new THREE.Mesh(postGeometry, postMaterial);
            post.position.set(xPos, 0.5, 0);
            post.castShadow = true;
            obstacleGroup.add(post);
        });
    }

    obstacleGroup.position.set(x, 0, z);
    obstacleGroup.userData.isObstacle = true;

    scene.add(obstacleGroup);
    obstacles.push(obstacleGroup);
}

function updatePlayer() {
    if (!gameActive) return;

    let moved = false;

    if (keys.ArrowLeft && player.position.x > -GAME_WIDTH / 2 + 1) {
        player.position.x -= PLAYER_SPEED;
        moved = true;
    }
    if (keys.ArrowRight && player.position.x < GAME_WIDTH / 2 - 1) {
        player.position.x += PLAYER_SPEED;
        moved = true;
    }
    if (keys.ArrowUp && player.position.z > -GAME_DEPTH) {
        player.position.z -= PLAYER_SPEED;
        moved = true;
    }
    if (keys.ArrowDown && player.position.z < 5) {
        player.position.z += PLAYER_SPEED;
        moved = true;
    }

    // Slight rotation when moving
    if (moved) {
        if (keys.ArrowLeft) player.rotation.y = Math.PI / 16;
        else if (keys.ArrowRight) player.rotation.y = -Math.PI / 16;
        else player.rotation.y *= 0.9;
    }

    // Camera follows player
    camera.position.x = player.position.x;
    camera.position.z = player.position.z + 5;
    camera.lookAt(player.position.x, 0, player.position.z - 5);
}

function spawnObjects() {
    if (!gameActive) return;

    // Spawn garages
    if (Math.random() < GARAGE_SPAWN_RATE) {
        const x = (Math.random() - 0.5) * (GAME_WIDTH - 4);
        const z = player.position.z - SPAWN_DISTANCE;
        createGarage(x, z);
    }

    // Spawn obstacles
    if (Math.random() < OBSTACLE_SPAWN_RATE) {
        const x = (Math.random() - 0.5) * (GAME_WIDTH - 2);
        const z = player.position.z - SPAWN_DISTANCE;
        createObstacle(x, z);
    }
}

function checkCollisions() {
    if (!gameActive) return;

    const playerBox = new THREE.Box3().setFromObject(player);

    // Check garage collisions (scoring)
    garages.forEach((garage, index) => {
        const garageBox = new THREE.Box3().setFromObject(garage);
        if (playerBox.intersectsBox(garageBox)) {
            // Successfully parked!
            score += 10;
            parksCount++;
            updateScore();
            showMessage('Odlično parkiranje! +10');

            // Remove garage
            scene.remove(garage);
            garages.splice(index, 1);
        }
    });

    // Check obstacle collisions (game over)
    obstacles.forEach(obstacle => {
        const obstacleBox = new THREE.Box3().setFromObject(obstacle);
        if (playerBox.intersectsBox(obstacleBox)) {
            gameOver();
        }
    });
}

function cleanupObjects() {
    // Remove objects that are behind the player
    const cleanupDistance = player.position.z + 10;

    garages = garages.filter(garage => {
        if (garage.position.z > cleanupDistance) {
            scene.remove(garage);
            return false;
        }
        return true;
    });

    obstacles = obstacles.filter(obstacle => {
        if (obstacle.position.z > cleanupDistance) {
            scene.remove(obstacle);
            return false;
        }
        return true;
    });
}

function updateScore() {
    document.getElementById('score').textContent = score;

    if (score > highScore) {
        highScore = score;
        localStorage.setItem('garageGameHighScore', highScore);
        document.getElementById('high-score').textContent = highScore;
    }
}

function startTimer() {
    setInterval(() => {
        if (gameActive) {
            time++;
            document.getElementById('time').textContent = time + 's';
        }
    }, 1000);
}

function showMessage(text) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.style.display = 'block';

    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 2000);
}

function gameOver() {
    gameActive = false;

    document.getElementById('final-score').textContent = score;
    document.getElementById('parks-count').textContent = parksCount;
    document.getElementById('game-over').style.display = 'block';
}

function restartGame() {
    // Reset game state
    score = 0;
    time = 0;
    parksCount = 0;
    gameActive = true;

    // Reset UI
    updateScore();
    document.getElementById('time').textContent = '0s';
    document.getElementById('game-over').style.display = 'none';

    // Reset player position
    player.position.set(0, 0, 0);
    player.rotation.y = 0;

    // Clear all objects
    garages.forEach(garage => scene.remove(garage));
    obstacles.forEach(obstacle => scene.remove(obstacle));
    garages = [];
    obstacles = [];
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    updatePlayer();
    spawnObjects();
    checkCollisions();
    cleanupObjects();

    renderer.render(scene, camera);
}

// Start the game
init();
