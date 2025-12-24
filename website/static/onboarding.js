/**
 * Onboarding Tour System for CozmicLearning
 * Interactive guided tour for new users
 */

(function() {
    'use strict';

    // Onboarding tours configuration
    const TOURS = {
        student: [
            {
                target: '.subjects-link, [href="/subjects"]',
                title: 'Welcome to CozmicLearning! 🚀',
                content: 'Let\'s take a quick tour to show you around. Click "Next" to continue or "Skip Tour" to explore on your own.',
                position: 'bottom'
            },
            {
                target: '.arcade-link, [href="/arcade"]',
                title: 'Play & Learn! 🎮',
                content: 'Visit the Arcade to play educational games, earn badges, and compete on leaderboards!',
                position: 'bottom'
            },
            {
                target: '.assignments-link, [href*="assignments"]',
                title: 'Your Assignments 📚',
                content: 'Check here for assignments from your teacher. Complete them to earn points and improve your skills!',
                position: 'bottom'
            },
            {
                target: '.character-selector, .profile-menu',
                title: 'Customize Your Experience ✨',
                content: 'Choose your AI tutor character and track your progress, badges, and achievements!',
                position: 'left'
            },
            {
                target: 'body',
                title: 'Keyboard Shortcuts ⌨️',
                content: 'Pro tip: Press <kbd>?</kbd> anytime to see keyboard shortcuts for faster navigation!',
                position: 'center'
            }
        ],

        teacher: [
            {
                target: 'body',
                title: 'Welcome, Teacher! 👨‍🏫',
                content: 'Let\'s get you set up! This quick tour will show you the main features.',
                position: 'center'
            },
            {
                target: '.classes-link, [href*="classes"]',
                title: 'Manage Your Classes',
                content: 'Create classes, generate join codes, and manage your students all in one place.',
                position: 'bottom'
            },
            {
                target: '.assignments-link, [href*="assignments"]',
                title: 'Create Assignments',
                content: 'Use AI to generate custom assignments with differentiation modes for different learning levels!',
                position: 'bottom'
            },
            {
                target: '.gradebook-link, [href*="gradebook"]',
                title: 'Track Progress',
                content: 'View student submissions, grade assignments, and track class performance.',
                position: 'bottom'
            },
            {
                target: '.messages-link, [href*="messages"]',
                title: 'Communicate with Parents',
                content: 'Send progress reports and messages directly to parents.',
                position: 'bottom'
            }
        ],

        parent: [
            {
                target: 'body',
                title: 'Welcome, Parent! 👨‍👩‍👧‍👦',
                content: 'Monitor your child\'s progress and stay connected with their learning journey!',
                position: 'center'
            },
            {
                target: '.analytics-link, [href*="analytics"]',
                title: 'Student Progress',
                content: 'View detailed analytics on how your children are performing across all subjects.',
                position: 'bottom'
            },
            {
                target: '.time-limits-link, [href*="time"]',
                title: 'Set Time Limits',
                content: 'Control how much time your children spend on CozmicLearning each day.',
                position: 'bottom'
            },
            {
                target: '.messages-link, [href*="messages"]',
                title: 'Teacher Communication',
                content: 'Receive updates from teachers and respond to messages about your child\'s progress.',
                position: 'bottom'
            },
            {
                target: '.safety-link, [href*="safety"]',
                title: 'Safety Settings',
                content: 'Review content moderation settings and keep your children safe online.',
                position: 'bottom'
            }
        ]
    };

    let currentTour = null;
    let currentStep = 0;
    let tourOverlay = null;
    let tourTooltip = null;

    // Initialize onboarding
    function init() {
        // Check if user has completed onboarding
        const userRole = document.body.dataset.userRole;
        const onboardingKey = `onboarding_completed_${userRole}`;
        const completed = localStorage.getItem(onboardingKey);

        if (!completed && TOURS[userRole]) {
            // Wait a bit for page to load
            setTimeout(() => {
                startTour(userRole);
            }, 1000);
        }
    }

    // Start a tour
    function startTour(tourName) {
        currentTour = TOURS[tourName];
        if (!currentTour) return;

        currentStep = 0;
        createTourElements();
        showStep(0);
    }

    // Create tour overlay and tooltip elements
    function createTourElements() {
        // Create overlay
        tourOverlay = document.createElement('div');
        tourOverlay.className = 'onboarding-overlay';
        tourOverlay.innerHTML = '<div class="onboarding-spotlight"></div>';
        document.body.appendChild(tourOverlay);

        // Create tooltip
        tourTooltip = document.createElement('div');
        tourTooltip.className = 'onboarding-tooltip';
        document.body.appendChild(tourTooltip);
    }

    // Show a specific step
    function showStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= currentTour.length) {
            endTour();
            return;
        }

        currentStep = stepIndex;
        const step = currentTour[stepIndex];

        // Find target element
        let target = null;
        if (step.target !== 'body') {
            target = document.querySelector(step.target);
            if (!target) {
                // Target not found, skip to next
                console.warn(`Onboarding target not found: ${step.target}`);
                showStep(stepIndex + 1);
                return;
            }
        }

        // Position spotlight
        positionSpotlight(target);

        // Update tooltip content
        updateTooltip(step, stepIndex);

        // Position tooltip
        positionTooltip(target, step.position);

        // Show elements
        tourOverlay.classList.add('active');
        tourTooltip.classList.add('active');
    }

    // Position spotlight on target
    function positionSpotlight(target) {
        const spotlight = tourOverlay.querySelector('.onboarding-spotlight');

        if (!target) {
            // Center spotlight
            spotlight.style.width = '0';
            spotlight.style.height = '0';
            spotlight.style.top = '50%';
            spotlight.style.left = '50%';
            return;
        }

        const rect = target.getBoundingClientRect();
        const padding = 10;

        spotlight.style.width = `${rect.width + padding * 2}px`;
        spotlight.style.height = `${rect.height + padding * 2}px`;
        spotlight.style.top = `${rect.top - padding + window.scrollY}px`;
        spotlight.style.left = `${rect.left - padding}px`;
        spotlight.style.borderRadius = window.getComputedStyle(target).borderRadius || '12px';
    }

    // Update tooltip content
    function updateTooltip(step, stepIndex) {
        const isFirst = stepIndex === 0;
        const isLast = stepIndex === currentTour.length - 1;

        tourTooltip.innerHTML = `
            <div class="onboarding-tooltip-header">
                <h3>${step.title}</h3>
                <button class="onboarding-close" onclick="window.Onboarding.skip()">×</button>
            </div>
            <div class="onboarding-tooltip-body">
                <p>${step.content}</p>
            </div>
            <div class="onboarding-tooltip-footer">
                <div class="onboarding-progress">
                    ${currentTour.map((_, i) => `
                        <span class="onboarding-dot ${i === stepIndex ? 'active' : ''}"></span>
                    `).join('')}
                </div>
                <div class="onboarding-actions">
                    ${!isFirst ? '<button class="onboarding-btn onboarding-btn-secondary" onclick="window.Onboarding.prev()">Back</button>' : ''}
                    <button class="onboarding-btn onboarding-btn-skip" onclick="window.Onboarding.skip()">Skip Tour</button>
                    <button class="onboarding-btn onboarding-btn-primary" onclick="window.Onboarding.next()">
                        ${isLast ? 'Get Started!' : 'Next'}
                    </button>
                </div>
            </div>
        `;
    }

    // Position tooltip relative to target
    function positionTooltip(target, position) {
        if (!target) {
            // Center on screen
            tourTooltip.style.top = '50%';
            tourTooltip.style.left = '50%';
            tourTooltip.style.transform = 'translate(-50%, -50%)';
            return;
        }

        const rect = target.getBoundingClientRect();
        const tooltipRect = tourTooltip.getBoundingClientRect();
        const spacing = 20;

        let top, left;

        switch (position) {
            case 'top':
                top = rect.top - tooltipRect.height - spacing + window.scrollY;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
                break;
            case 'bottom':
                top = rect.bottom + spacing + window.scrollY;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
                break;
            case 'left':
                top = rect.top + (rect.height - tooltipRect.height) / 2 + window.scrollY;
                left = rect.left - tooltipRect.width - spacing;
                break;
            case 'right':
                top = rect.top + (rect.height - tooltipRect.height) / 2 + window.scrollY;
                left = rect.right + spacing;
                break;
            default:
                top = rect.bottom + spacing + window.scrollY;
                left = rect.left + (rect.width - tooltipRect.width) / 2;
        }

        // Keep tooltip on screen
        const maxLeft = window.innerWidth - tooltipRect.width - 20;
        left = Math.max(20, Math.min(left, maxLeft));

        tourTooltip.style.top = `${top}px`;
        tourTooltip.style.left = `${left}px`;
        tourTooltip.style.transform = 'none';
    }

    // Navigation functions
    function next() {
        showStep(currentStep + 1);
    }

    function prev() {
        showStep(currentStep - 1);
    }

    function skip() {
        if (confirm('Are you sure you want to skip the tour? You can always restart it from settings.')) {
            endTour();
        }
    }

    // End tour
    function endTour() {
        if (tourOverlay) {
            tourOverlay.remove();
            tourOverlay = null;
        }
        if (tourTooltip) {
            tourTooltip.remove();
            tourTooltip = null;
        }

        // Mark as completed
        const userRole = document.body.dataset.userRole;
        if (userRole) {
            localStorage.setItem(`onboarding_completed_${userRole}`, 'true');
        }

        currentTour = null;
        currentStep = 0;
    }

    // Public API
    window.Onboarding = {
        start: function(tourName) {
            tourName = tourName || document.body.dataset.userRole;
            startTour(tourName);
        },
        next: next,
        prev: prev,
        skip: skip,
        reset: function() {
            const userRole = document.body.dataset.userRole;
            if (userRole) {
                localStorage.removeItem(`onboarding_completed_${userRole}`);
                window.location.reload();
            }
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Handle window resize
    window.addEventListener('resize', () => {
        if (currentTour && currentStep < currentTour.length) {
            showStep(currentStep);
        }
    });

})();
