// Black Hole Collision - Gravitational Waves Game
let scene, camera, renderer;
let player, ground;
let blackHole1, blackHole2;
let gravitationalWaves = [];
let stars = [];
let score = 0;
let time = 0;
let gameActive = true;
let highScore = 0;
let wavesJumped = 0;

// Game settings
const PLAYER_SPEED = 0.2;
const JUMP_FORCE = 0.35;
const GRAVITY = 0.015;
const WAVE_SPEED = 0.12;
const WAVE_SPAWN_INTERVAL = 90; // frames between waves
const GROUND_Y = -2;
const PLAYER_RADIUS = 0.4;

// Player physics
let playerVelocityY = 0;
let isJumping = false;
let frameCount = 0;
let collisionPhase = 0;

// Input
const keys = {
    ArrowLeft: false,
    ArrowRight: false,
    ArrowUp: false,
    Space: false
};

// Initialize the game
function init() {
    // Load high score
    highScore = parseInt(localStorage.getItem('blackHoleGameHighScore') || '0');
    document.getElementById('high-score').textContent = highScore;

    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    scene.fog = new THREE.FogExp2(0x000011, 0.015);

    // Camera setup
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 2, 12);
    camera.lookAt(0, 0, 0);

    // Renderer setup
    const canvas = document.getElementById('canvas');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x4444ff, 0.3);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x8888ff, 0.8, 100);
    pointLight.position.set(0, 10, 10);
    scene.add(pointLight);

    // Create starfield
    createStarfield();

    // Ground (platform)
    const groundGeometry = new THREE.BoxGeometry(15, 0.5, 50);
    const groundMaterial = new THREE.MeshStandardMaterial({
        color: 0x1a0033,
        emissive: 0x110022,
        roughness: 0.8,
        metalness: 0.3
    });
    ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.position.y = GROUND_Y;
    scene.add(ground);

    // Ground grid lines
    for (let i = -7; i <= 7; i += 1) {
        const lineGeometry = new THREE.BoxGeometry(0.05, 0.05, 50);
        const lineMaterial = new THREE.MeshBasicMaterial({
            color: 0x4400ff,
            transparent: true,
            opacity: 0.3
        });
        const line = new THREE.Mesh(lineGeometry, lineMaterial);
        line.position.set(i, GROUND_Y + 0.3, 0);
        scene.add(line);
    }

    // Player (astronaut/sphere)
    createPlayer();

    // Black holes
    createBlackHoles();

    // Event listeners
    window.addEventListener('keydown', (e) => {
        if (e.key === ' ') {
            keys.Space = true;
            e.preventDefault();
        } else if (keys.hasOwnProperty(e.key)) {
            keys[e.key] = true;
            e.preventDefault();
        }
    });

    window.addEventListener('keyup', (e) => {
        if (e.key === ' ') {
            keys.Space = false;
        } else if (keys.hasOwnProperty(e.key)) {
            keys[e.key] = false;
        }
    });

    window.addEventListener('resize', onWindowResize);

    document.getElementById('restart-btn').addEventListener('click', restartGame);

    // Start game loop
    animate();
    startTimer();
}

function createStarfield() {
    const starGeometry = new THREE.BufferGeometry();
    const starVertices = [];

    for (let i = 0; i < 1000; i++) {
        const x = (Math.random() - 0.5) * 200;
        const y = (Math.random() - 0.5) * 200;
        const z = (Math.random() - 0.5) * 200;
        starVertices.push(x, y, z);
    }

    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));

    const starMaterial = new THREE.PointsMaterial({
        color: 0xffffff,
        size: 0.3,
        transparent: true,
        opacity: 0.8
    });

    const starField = new THREE.Points(starGeometry, starMaterial);
    scene.add(starField);
    stars.push(starField);
}

function createPlayer() {
    const playerGroup = new THREE.Group();

    // Main body (sphere)
    const bodyGeometry = new THREE.SphereGeometry(PLAYER_RADIUS, 32, 32);
    const bodyMaterial = new THREE.MeshStandardMaterial({
        color: 0x00ffff,
        emissive: 0x00aaaa,
        metalness: 0.8,
        roughness: 0.2
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    playerGroup.add(body);

    // Glow ring
    const ringGeometry = new THREE.TorusGeometry(PLAYER_RADIUS + 0.1, 0.05, 16, 32);
    const ringMaterial = new THREE.MeshBasicMaterial({
        color: 0x00ffff,
        transparent: true,
        opacity: 0.6
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.x = Math.PI / 2;
    playerGroup.add(ring);

    playerGroup.position.set(0, GROUND_Y + 1, 0);
    player = playerGroup;
    scene.add(player);
}

function createBlackHoles() {
    // Black Hole 1 (left)
    const blackHole1Group = new THREE.Group();

    // Core
    const core1Geometry = new THREE.SphereGeometry(1.5, 32, 32);
    const core1Material = new THREE.MeshBasicMaterial({
        color: 0x000000
    });
    const core1 = new THREE.Mesh(core1Geometry, core1Material);
    blackHole1Group.add(core1);

    // Accretion disk
    const disk1Geometry = new THREE.TorusGeometry(2.5, 0.4, 16, 64);
    const disk1Material = new THREE.MeshBasicMaterial({
        color: 0xff6600,
        transparent: true,
        opacity: 0.7
    });
    const disk1 = new THREE.Mesh(disk1Geometry, disk1Material);
    disk1.rotation.x = Math.PI / 2.3;
    blackHole1Group.add(disk1);

    // Glow
    const glow1Geometry = new THREE.SphereGeometry(2, 32, 32);
    const glow1Material = new THREE.MeshBasicMaterial({
        color: 0xff4400,
        transparent: true,
        opacity: 0.3
    });
    const glow1 = new THREE.Mesh(glow1Geometry, glow1Material);
    blackHole1Group.add(glow1);

    blackHole1Group.position.set(-8, 8, -15);
    blackHole1 = blackHole1Group;
    scene.add(blackHole1);

    // Black Hole 2 (right)
    const blackHole2Group = new THREE.Group();

    const core2 = new THREE.Mesh(core1Geometry, core1Material);
    blackHole2Group.add(core2);

    const disk2Geometry = new THREE.TorusGeometry(2.5, 0.4, 16, 64);
    const disk2Material = new THREE.MeshBasicMaterial({
        color: 0x0088ff,
        transparent: true,
        opacity: 0.7
    });
    const disk2 = new THREE.Mesh(disk2Geometry, disk2Material);
    disk2.rotation.x = Math.PI / 2.3;
    blackHole2Group.add(disk2);

    const glow2 = new THREE.Mesh(glow1Geometry.clone(), glow1Material.clone());
    glow2.material.color.set(0x0066ff);
    blackHole2Group.add(glow2);

    blackHole2Group.position.set(8, 8, -15);
    blackHole2 = blackHole2Group;
    scene.add(blackHole2);
}

function updateBlackHoles() {
    if (!blackHole1 || !blackHole2) return;

    // Rotate accretion disks
    blackHole1.children[1].rotation.z += 0.02;
    blackHole2.children[1].rotation.z -= 0.02;

    // Pulse glow
    const pulseScale = 1 + Math.sin(frameCount * 0.05) * 0.1;
    blackHole1.children[2].scale.set(pulseScale, pulseScale, pulseScale);
    blackHole2.children[2].scale.set(pulseScale, pulseScale, pulseScale);

    // Move black holes towards each other (orbital and collision)
    collisionPhase += 0.0005;

    const orbitRadius = 8 - collisionPhase * 5;
    const angle = frameCount * 0.01;

    if (orbitRadius > 1) {
        blackHole1.position.x = -orbitRadius * Math.cos(angle);
        blackHole1.position.z = -15 + orbitRadius * Math.sin(angle) * 0.5;

        blackHole2.position.x = orbitRadius * Math.cos(angle);
        blackHole2.position.z = -15 - orbitRadius * Math.sin(angle) * 0.5;
    } else {
        // Merged state - oscillate
        const mergeX = Math.sin(frameCount * 0.03) * 0.5;
        blackHole1.position.set(mergeX, 8, -15);
        blackHole2.position.set(mergeX, 8, -15);
    }
}

function createGravitationalWave(side) {
    const waveGroup = new THREE.Group();

    // Main wave ring
    const ringGeometry = new THREE.TorusGeometry(2, 0.15, 16, 32);
    const ringMaterial = new THREE.MeshBasicMaterial({
        color: side === 'left' ? 0xff6600 : 0x0088ff,
        transparent: true,
        opacity: 0.8,
        emissive: side === 'left' ? 0xff4400 : 0x0066ff
    });
    const ring = new THREE.Mesh(ringGeometry, ringMaterial);
    ring.rotation.y = Math.PI / 2;
    waveGroup.add(ring);

    // Inner glow ring
    const innerRingGeometry = new THREE.TorusGeometry(1.5, 0.1, 16, 32);
    const innerRingMaterial = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.5
    });
    const innerRing = new THREE.Mesh(innerRingGeometry, innerRingMaterial);
    innerRing.rotation.y = Math.PI / 2;
    waveGroup.add(innerRing);

    // Position wave
    const startX = side === 'left' ? blackHole1.position.x : blackHole2.position.x;
    waveGroup.position.set(startX, 0, -10);

    waveGroup.userData.side = side;
    waveGroup.userData.passed = false;

    scene.add(waveGroup);
    gravitationalWaves.push(waveGroup);
}

function updatePlayer() {
    if (!gameActive) return;

    // Horizontal movement
    if (keys.ArrowLeft && player.position.x > -6.5) {
        player.position.x -= PLAYER_SPEED;
    }
    if (keys.ArrowRight && player.position.x < 6.5) {
        player.position.x += PLAYER_SPEED;
    }

    // Jump
    if ((keys.ArrowUp || keys.Space) && !isJumping) {
        playerVelocityY = JUMP_FORCE;
        isJumping = true;
    }

    // Apply gravity
    playerVelocityY -= GRAVITY;
    player.position.y += playerVelocityY;

    // Ground collision
    if (player.position.y <= GROUND_Y + 1) {
        player.position.y = GROUND_Y + 1;
        playerVelocityY = 0;
        isJumping = false;
    }

    // Rotate player when moving
    if (keys.ArrowLeft || keys.ArrowRight) {
        player.rotation.y += 0.1;
    }

    // Pulse the player ring
    if (player.children[1]) {
        player.children[1].rotation.z += 0.05;
        const scale = 1 + Math.sin(frameCount * 0.1) * 0.1;
        player.children[1].scale.set(scale, scale, scale);
    }
}

function spawnWaves() {
    if (!gameActive) return;

    frameCount++;

    // Spawn waves periodically
    if (frameCount % WAVE_SPAWN_INTERVAL === 0) {
        const side = Math.random() < 0.5 ? 'left' : 'right';
        createGravitationalWave(side);
    }
}

function updateWaves() {
    gravitationalWaves.forEach((wave, index) => {
        // Move wave towards player
        wave.position.z += WAVE_SPEED;

        // Expand wave as it travels
        const scale = 1 + (wave.position.z + 10) * 0.05;
        wave.scale.set(scale, scale, scale);

        // Fade out as it expands
        wave.children.forEach(child => {
            child.material.opacity = Math.max(0.2, 0.8 - (wave.position.z + 10) * 0.03);
        });

        // Rotate wave
        wave.rotation.z += 0.02;

        // Remove wave if it's behind the player
        if (wave.position.z > 15) {
            scene.remove(wave);
            gravitationalWaves.splice(index, 1);
        }
    });
}

function checkCollisions() {
    if (!gameActive) return;

    gravitationalWaves.forEach((wave, index) => {
        // Check if wave is at player's Z position
        const distanceZ = Math.abs(wave.position.z - player.position.z);

        if (distanceZ < 1 && !wave.userData.passed) {
            // Check if player is in the wave's path
            const distanceX = Math.abs(wave.position.x - player.position.x);
            const waveRadius = 2 * wave.scale.x;

            // Player is within the wave's horizontal range
            if (distanceX < waveRadius) {
                // Check if player jumped over it
                if (player.position.y > GROUND_Y + 2.5) {
                    // Successfully jumped!
                    wave.userData.passed = true;
                    score += 10;
                    wavesJumped++;
                    updateScore();
                    showMessage('Odličen skok! +10');
                } else {
                    // Hit the wave
                    gameOver();
                }
            }
        }

        // Mark waves that passed by
        if (wave.position.z > player.position.z + 2 && !wave.userData.passed) {
            wave.userData.passed = true;
            score += 5;
            updateScore();
        }
    });
}

function updateScore() {
    document.getElementById('score').textContent = score;

    if (score > highScore) {
        highScore = score;
        localStorage.setItem('blackHoleGameHighScore', highScore);
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
    document.getElementById('waves-count').textContent = wavesJumped;
    document.getElementById('game-over').style.display = 'block';
}

function restartGame() {
    // Reset game state
    score = 0;
    time = 0;
    wavesJumped = 0;
    gameActive = true;
    frameCount = 0;
    collisionPhase = 0;

    // Reset UI
    updateScore();
    document.getElementById('time').textContent = '0s';
    document.getElementById('game-over').style.display = 'none';

    // Reset player position
    player.position.set(0, GROUND_Y + 1, 0);
    playerVelocityY = 0;
    isJumping = false;

    // Clear all waves
    gravitationalWaves.forEach(wave => scene.remove(wave));
    gravitationalWaves = [];

    // Reset black holes
    scene.remove(blackHole1);
    scene.remove(blackHole2);
    createBlackHoles();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    updateBlackHoles();
    updatePlayer();
    spawnWaves();
    updateWaves();
    checkCollisions();

    // Rotate starfield slowly
    if (stars[0]) {
        stars[0].rotation.y += 0.0002;
    }

    renderer.render(scene, camera);
}

// Start the game
init();
