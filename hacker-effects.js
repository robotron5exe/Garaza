// Hacker/Terminal Effects JavaScript

// Matrix rain effect
function initMatrixEffect() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const matrixBg = document.getElementById('matrixBg');

    if (!matrixBg) return;

    matrixBg.appendChild(canvas);

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    const fontSize = 14;
    const columns = canvas.width / fontSize;

    const drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.random() * -100;
    }

    function drawMatrix() {
        ctx.fillStyle = 'rgba(10, 14, 26, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            const x = i * fontSize;
            const y = drops[i] * fontSize;

            ctx.fillText(char, x, y);

            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(drawMatrix, 50);

    // Resize handler
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Typing effect for text
function initTypingEffect() {
    const elements = document.querySelectorAll('.typing-effect');

    elements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        element.style.opacity = '1';

        let i = 0;
        const speed = 20;

        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }

        // Start typing when element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    type();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(element);
    });
}

// Add random glitch effect to certain elements
function initGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch');

    glitchElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                element.style.textShadow = `
                    ${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px #ff006e,
                    ${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px #00ffff
                `;

                setTimeout(() => {
                    element.style.textShadow = '0 0 20px rgba(0, 255, 65, 0.5)';
                }, 50);
            }
        }, 100);
    });
}

// Flicker effect for specific text
function initFlickerEffect() {
    const flickerElements = document.querySelectorAll('.status-ok, .prompt');

    flickerElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.98) {
                element.style.opacity = '0.5';
                setTimeout(() => {
                    element.style.opacity = '1';
                }, 50);
            }
        }, 200);
    });
}

// Add boot sequence animation
function initBootSequence() {
    const sections = document.querySelectorAll('.section');

    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';

        setTimeout(() => {
            section.style.transition = 'all 0.5s ease';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Random console messages
function initConsoleMessages() {
    const messages = [
        'System initialized...',
        'Loading quantum modules...',
        'Establishing secure connection...',
        'Analyzing probability distributions...',
        'Mathematical framework active...',
        'Statistical engines online...',
        'All systems operational'
    ];

    let messageIndex = 0;

    console.log('%c[SYSTEM]', 'color: #00ff41; font-weight: bold; font-size: 14px;');

    const interval = setInterval(() => {
        if (messageIndex < messages.length) {
            console.log(
                '%c' + messages[messageIndex],
                'color: #00ff41; font-family: monospace;'
            );
            messageIndex++;
        } else {
            clearInterval(interval);
            console.log(
                '%c[✓] All systems ready',
                'color: #00ff41; font-weight: bold; font-size: 14px;'
            );
        }
    }, 300);
}

// Add hover effect to cards
function initCardEffects() {
    const cards = document.querySelectorAll('.card, .app-item, .method');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
}

// Animate code blocks on scroll
function initCodeBlockAnimation() {
    const codeBlocks = document.querySelectorAll('.code-block');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideIn 0.5s ease';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    codeBlocks.forEach(block => {
        block.style.opacity = '0';
        block.style.transform = 'translateX(-20px)';
        observer.observe(block);
    });
}

// Add CSS animation for code blocks
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;
document.head.appendChild(style);

// Interactive terminal prompt
function initInteractivePrompt() {
    const promptLines = document.querySelectorAll('.prompt-line');

    promptLines.forEach(line => {
        line.addEventListener('click', () => {
            const command = line.querySelector('.command');
            if (command) {
                // Create selection effect
                command.style.background = 'rgba(0, 255, 65, 0.2)';
                setTimeout(() => {
                    command.style.background = 'transparent';
                }, 200);
            }
        });
    });
}

// Add easter egg - Konami code
function initEasterEgg() {
    const konamiCode = [
        'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
        'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
        'b', 'a'
    ];
    let konamiIndex = 0;

    document.addEventListener('keydown', (e) => {
        if (e.key === konamiCode[konamiIndex]) {
            konamiIndex++;

            if (konamiIndex === konamiCode.length) {
                // Easter egg activated!
                document.body.style.animation = 'rainbow 2s linear infinite';

                const style = document.createElement('style');
                style.textContent = `
                    @keyframes rainbow {
                        0% { filter: hue-rotate(0deg); }
                        100% { filter: hue-rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);

                console.log(
                    '%c🎉 KONAMI CODE ACTIVATED! 🎉',
                    'color: #ff006e; font-size: 20px; font-weight: bold;'
                );

                setTimeout(() => {
                    document.body.style.animation = '';
                }, 5000);

                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });
}

// Random data stream effect
function initDataStream() {
    const dataStreamEl = document.createElement('div');
    dataStreamEl.style.position = 'fixed';
    dataStreamEl.style.top = '0';
    dataStreamEl.style.right = '10px';
    dataStreamEl.style.color = 'rgba(0, 255, 65, 0.3)';
    dataStreamEl.style.fontSize = '10px';
    dataStreamEl.style.fontFamily = 'monospace';
    dataStreamEl.style.lineHeight = '1.2';
    dataStreamEl.style.zIndex = '5';
    dataStreamEl.style.pointerEvents = 'none';
    dataStreamEl.style.maxWidth = '100px';
    dataStreamEl.style.overflow = 'hidden';

    document.body.appendChild(dataStreamEl);

    function generateRandomData() {
        const chars = '0123456789ABCDEF';
        let output = '';
        for (let i = 0; i < 20; i++) {
            output += chars[Math.floor(Math.random() * chars.length)];
            if ((i + 1) % 4 === 0) output += '\n';
        }
        return output;
    }

    setInterval(() => {
        dataStreamEl.textContent = generateRandomData();
    }, 100);
}

// Initialize all effects
function initAll() {
    console.log(
        '%cInitializing hacker interface...',
        'color: #00ff41; font-family: monospace; font-size: 12px;'
    );

    initMatrixEffect();
    initTypingEffect();
    initGlitchEffect();
    initFlickerEffect();
    initBootSequence();
    initConsoleMessages();
    initCardEffects();
    initCodeBlockAnimation();
    initInteractivePrompt();
    initEasterEgg();

    // Uncomment for data stream (can be distracting)
    // initDataStream();

    console.log(
        '%c[✓] Interface ready',
        'color: #00ff41; font-weight: bold; font-family: monospace;'
    );
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
} else {
    initAll();
}

// Performance monitoring
if (window.performance) {
    window.addEventListener('load', () => {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;

        console.log(
            '%c[PERF] Page loaded in ' + pageLoadTime + 'ms',
            'color: #00ffff; font-family: monospace;'
        );
    });
}
