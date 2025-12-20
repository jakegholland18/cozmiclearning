/**
 * CozmicLearning UI Enhancements
 * Streaming responses, animations, character comments, and more
 */

// ================================================================
// TYPING INDICATOR
// ================================================================

function createTypingIndicator() {
    const div = document.createElement('div');
    div.className = 'typing-indicator';
    div.innerHTML = '<span></span><span></span><span></span>';
    return div;
}

// ================================================================
// CONFETTI EFFECT
// ================================================================

function launchConfetti(count = 50) {
    for (let i = 0; i < count; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.textContent = ['🎉', '⭐', '🚀', '✨', '🌟'][Math.floor(Math.random() * 5)];
        
        const tx = (Math.random() - 0.5) * 400;
        const ty = -Math.random() * 500 - 200;
        confetti.style.setProperty('--tx', `${tx}px`);
        confetti.style.setProperty('--ty', `${ty}px`);
        
        confetti.style.left = Math.random() * window.innerWidth + 'px';
        confetti.style.top = '50%';
        confetti.style.fontSize = (Math.random() * 1.5 + 1) + 'rem';
        
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 3000);
    }
}

function celebrationBurst() {
    launchConfetti(60);
    
    // Celebration emojis
    const emojis = ['🎊', '🏆', '💫', '🌈', '⚡'];
    for (let i = 0; i < 3; i++) {
        const burst = document.createElement('div');
        burst.className = 'celebration-burst';
        burst.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        burst.style.left = (Math.random() * 100) + 'vw';
        burst.style.top = (Math.random() * 100) + 'vh';
        document.body.appendChild(burst);
        setTimeout(() => burst.remove(), 800);
    }
}

// ================================================================
// STREAMING TEXT EFFECT (Character by character)
// ================================================================

async function streamText(element, text, speed = 30) {
    element.innerHTML = '';
    element.classList.add('ai-streaming');

    // Find the scrollable parent (chat log container)
    let scrollContainer = element.parentElement;
    while (scrollContainer && scrollContainer.scrollHeight <= scrollContainer.clientHeight) {
        scrollContainer = scrollContainer.parentElement;
    }

    for (let i = 0; i < text.length; i++) {
        element.textContent += text[i];

        // Auto-scroll during streaming if we found a scroll container
        if (scrollContainer) {
            scrollContainer.scrollTop = scrollContainer.scrollHeight;
        }

        await new Promise(resolve => setTimeout(resolve, speed));
    }

    element.classList.remove('ai-streaming');

    // Final scroll to ensure we're at the bottom
    if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
}

// ================================================================
// FLOATING HELP BUTTON
// ================================================================

function initializeHelpButton() {
    // Check if button already exists
    if (document.getElementById('floating-help-btn')) return;
    
    const button = document.createElement('button');
    button.id = 'floating-help-btn';
    button.className = 'floating-help-btn';
    button.textContent = '?';
    button.setAttribute('aria-label', 'Help');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'help-tooltip';
    tooltip.style.display = 'none';
    
    // Update tooltip content based on current page
    const updateTooltip = () => {
        const path = window.location.pathname;
        let helpText = 'Need help? Click on any feature to learn more!';
        
        if (path.includes('/dashboard')) {
            helpText = '📊 Check your progress, earn XP, and level up! Streaks reward consistency.';
        } else if (path.includes('/practice')) {
            helpText = '🎯 Answer questions at your level. Get hints when stuck, keep learning!';
        } else if (path.includes('/teacher')) {
            helpText = '👨‍🏫 Create assignments, preview AI missions, and track student progress.';
        } else if (path.includes('/subject')) {
            helpText = '🌍 Explore different subjects! Each planet has unique learning content.';
        }
        
        tooltip.textContent = helpText;
    };
    
    updateTooltip();
    
    button.addEventListener('click', () => {
        if (tooltip.style.display === 'none') {
            tooltip.style.display = 'block';
            updateTooltip();
        } else {
            tooltip.style.display = 'none';
        }
    });
    
    // Close tooltip when clicking outside
    document.addEventListener('click', (e) => {
        if (!button.contains(e.target) && !tooltip.contains(e.target)) {
            tooltip.style.display = 'none';
        }
    });
    
    button.appendChild(tooltip);
    document.body.appendChild(button);
}

// ================================================================
// CHARACTER PERSONALITY COMMENTS
// ================================================================

const characterVoices = {
    everly: {
        levelUp: "✨ Wow! You're becoming quite the scholar, just like a true brave warrior!",
        missionComplete: "🌟 Your wisdom shines brightly! Well done on completing this quest!",
        streakCongrats: "💫 An unstoppable streak! Your dedication inspires me!",
        encouragement: "💪 I believe in you! Keep pushing forward with courage!",
    },
    nova: {
        levelUp: "⚡ LEVEL UP! Your learning engine is firing on all cylinders!",
        missionComplete: "🚀 Mission accomplished! Your curiosity is electrifying!",
        streakCongrats: "🔥 On FIRE! This streak is absolutely legendary!",
        encouragement: "🤖 Keep the momentum going! You're unstoppable!",
    },
    lio: {
        levelUp: "🎯 Sharp move! Your ability has advanced magnificently.",
        missionComplete: "✅ A flawless execution. Mission complete with confidence.",
        streakCongrats: "🏆 Your commitment speaks volumes. Impressive streak!",
        encouragement: "💎 Steady and focused. You're on the right path.",
    },
    jasmine: {
        levelUp: "🌈 Yay! You're growing so wonderfully! I'm so proud of you!",
        missionComplete: "💖 Absolutely amazing work! You light up the whole galaxy!",
        streakCongrats: "✨ What a beautiful streak! Your spirit is radiant!",
        encouragement: "🌸 You've got this! I'm cheering for you every step!",
    },
    theo: {
        levelUp: "📚 Excellent progress. Your understanding deepens nicely.",
        missionComplete: "🧠 A thoughtful completion. Your reasoning is sound.",
        streakCongrats: "📖 Consistency is wisdom. Your streak reflects dedication.",
        encouragement: "🎓 Take your time. Learning is a journey, not a race.",
    },
};

function showCharacterComment(commentType, character = 'everly') {
    if (!characterVoices[character] || !characterVoices[character][commentType]) {
        return;
    }
    
    const comment = characterVoices[character][commentType];
    const commentBox = document.createElement('div');
    commentBox.className = 'character-comment';
    commentBox.textContent = comment;
    
    // Find appropriate container (dashboard, assignment complete, etc.)
    const container = document.querySelector('.overview-box') || 
                     document.querySelector('.dashboard-content') ||
                     document.querySelector('main') ||
                     document.body;
    
    // Insert at top of container or after first heading
    const firstHeading = container.querySelector('h1, h2');
    if (firstHeading && firstHeading.nextElementSibling) {
        firstHeading.parentNode.insertBefore(commentBox, firstHeading.nextElementSibling);
    } else {
        container.insertBefore(commentBox, container.firstChild);
    }
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        commentBox.style.opacity = '0';
        commentBox.style.transition = 'opacity 0.3s ease';
        setTimeout(() => commentBox.remove(), 300);
    }, 8000);
}

// ================================================================
// DIFFICULTY BADGE HELPER
// ================================================================

function getDifficultyBadgeClass(difficulty) {
    if (!difficulty) return 'difficulty-medium';
    
    const d = difficulty.toLowerCase();
    if (d.includes('easy') || d.includes('beginner')) return 'difficulty-easy';
    if (d.includes('hard') || d.includes('advanced')) return 'difficulty-hard';
    return 'difficulty-medium';
}

function createDifficultyBadge(difficulty) {
    const badge = document.createElement('span');
    badge.className = `difficulty-badge ${getDifficultyBadgeClass(difficulty)}`;
    badge.textContent = difficulty || 'Medium';
    return badge;
}

// ================================================================
// PROGRESS BAR
// ================================================================

function createProgressBar(current, total) {
    const container = document.createElement('div');
    container.className = 'mission-progress';
    
    const label = document.createElement('div');
    label.style.marginBottom = '10px';
    label.style.fontSize = '0.95rem';
    label.style.opacity = '0.9';
    label.textContent = `Question ${current} of ${total}`;
    
    const outer = document.createElement('div');
    outer.className = 'progress-bar-outer';
    
    const inner = document.createElement('div');
    inner.className = 'progress-bar-inner';
    inner.style.width = `${(current / total) * 100}%`;
    
    outer.appendChild(inner);
    container.appendChild(label);
    container.appendChild(outer);
    
    return container;
}

// ================================================================
// WARM BUTTON TEXT REPLACEMENTS
// ================================================================

function makeButtonsFriendly() {
    const buttonReplacements = {
        'Submit': '✅ I think it\'s...',
        'Next': '➜ Ready for the next one?',
        'Submit Answer': '✅ I think it\'s...',
        'Continue': '➜ Let\'s keep going',
        'Start': '🚀 Let\'s dive in!',
        'Send': '📤 Share my thoughts',
        'Create': '✨ Create it!',
        'Save': '💾 Save my work',
        'Delete': '🗑️ Remove it',
        'Edit': '✏️ Edit',
        'Cancel': '❌ Never mind',
    };
    
    document.querySelectorAll('button, a.btn, input[type="submit"]').forEach(btn => {
        const text = btn.textContent.trim();
        if (buttonReplacements[text]) {
            btn.textContent = buttonReplacements[text];
        }
    });
}

// ================================================================
// INITIALIZATION
// ================================================================

// ================================================================
// ACHIEVEMENT UNLOCK POPUP
// ================================================================

function showAchievementUnlock(icon, name, description) {
    // Create achievement popup
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="achievement-icon">${icon}</div>
        <div class="achievement-content">
            <div class="achievement-title">Achievement Unlocked!</div>
            <div class="achievement-name">${name}</div>
            <div class="achievement-desc">${description}</div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    // Trigger animation
    setTimeout(() => popup.classList.add('show'), 100);
    
    // Launch confetti
    launchConfetti(40);
    
    // Remove after 5 seconds
    setTimeout(() => {
        popup.classList.remove('show');
        setTimeout(() => popup.remove(), 500);
    }, 5000);
}

// ================================================================
// GLOBAL ENTER KEY SUBMISSION
// ================================================================

function initializeEnterKeySubmission() {
    // Add Enter key support for all textareas and text inputs
    document.addEventListener('keydown', (e) => {
        // Only handle Enter key
        if (e.key !== 'Enter') return;

        const target = e.target;

        // Handle textareas (Enter without Shift submits)
        if (target.tagName === 'TEXTAREA') {
            // Skip if Shift is held (allow multi-line)
            if (e.shiftKey) return;

            // Find the closest form
            const form = target.closest('form');
            if (form) {
                e.preventDefault();
                form.submit();
            }
        }

        // Handle text/email/url inputs (Enter always submits)
        if (target.tagName === 'INPUT' &&
            (target.type === 'text' || target.type === 'email' ||
             target.type === 'url' || target.type === 'search')) {
            const form = target.closest('form');
            if (form) {
                e.preventDefault();
                form.submit();
            }
        }
    });
}

// ================================================================
// BACK TO DASHBOARD BUTTON
// ================================================================

function initializeDashboardButton() {
    // Don't add button on dashboard pages themselves
    const currentPath = window.location.pathname;
    if (currentPath.includes('/dashboard') ||
        currentPath === '/' ||
        currentPath.includes('/login') ||
        currentPath.includes('/signup')) {
        return;
    }

    // Determine which dashboard URL to use based on user role
    let dashboardUrl = null;
    let dashboardLabel = null;

    // Check navigation links to determine user type
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;

    if (navLinks.querySelector('a[href="/dashboard"]')) {
        // Student
        dashboardUrl = '/dashboard';
        dashboardLabel = '🏠 Back to Student Dashboard';
    } else if (navLinks.querySelector('a[href="/parent_dashboard"]')) {
        // Parent
        dashboardUrl = '/parent_dashboard';
        dashboardLabel = '🏠 Back to Parent Dashboard';
    } else if (navLinks.querySelector('a[href="/teacher/dashboard"]')) {
        // Teacher
        dashboardUrl = '/teacher/dashboard';
        dashboardLabel = '🏠 Back to Teacher Dashboard';
    }

    if (!dashboardUrl) return;

    // Create button container
    const container = document.createElement('div');
    container.className = 'dashboard-btn-container';

    // Create button
    const button = document.createElement('a');
    button.href = dashboardUrl;
    button.className = 'back-to-dashboard';
    button.innerHTML = `<span>←</span><span>${dashboardLabel}</span>`;

    container.appendChild(button);

    // Insert at the beginning of the main content area
    const contentContainer = document.querySelector('.container');
    if (contentContainer && contentContainer.firstChild) {
        contentContainer.insertBefore(container, contentContainer.firstChild);
    }
}

// ================================================================
// INIT & EXPORTS
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeHelpButton();
    makeButtonsFriendly();
    initializeEnterKeySubmission();
    initializeDashboardButton();
});

// Export for use in inline scripts
window.CozmicEnhancements = {
    launchConfetti,
    celebrationBurst,
    streamText,
    showCharacterComment,
    createProgressBar,
    createDifficultyBadge,
    createTypingIndicator,
    showAchievementUnlock,
};
