/**
 * Global Keyboard Shortcuts for CozmicLearning
 * Provides keyboard navigation and power user features
 */

(function() {
    'use strict';

    // Keyboard shortcuts configuration
    const shortcuts = {
        // Global navigation
        'g d': { action: goToDashboard, description: 'Go to Dashboard', global: true },
        'g s': { action: goToSubjects, description: 'Go to Subjects', global: true },
        'g a': { action: goToArcade, description: 'Go to Arcade', global: true },
        'g t': { action: goToTutorials, description: 'Go to Tutorials', global: true },

        // Assignment shortcuts
        'n': { action: nextQuestion, description: 'Next question', context: 'assignment' },
        'p': { action: previousQuestion, description: 'Previous question', context: 'assignment' },
        's': { action: submitAnswer, description: 'Submit answer', context: 'assignment' },
        'h': { action: showHint, description: 'Show hint', context: 'assignment' },

        // General shortcuts
        '/': { action: focusSearch, description: 'Focus search', global: true },
        '?': { action: showShortcutHelp, description: 'Show keyboard shortcuts', global: true },
        'esc': { action: closeModal, description: 'Close modal/dialog', global: true },

        // Teacher shortcuts
        'g c': { action: goToClasses, description: 'Go to Classes', role: 'teacher' },
        'g g': { action: goToGradebook, description: 'Go to Gradebook', role: 'teacher' },
        'c a': { action: createAssignment, description: 'Create Assignment', role: 'teacher' },

        // Parent shortcuts
        'g p': { action: goToProgress, description: 'Go to Progress', role: 'parent' },
        'g m': { action: goToMessages, description: 'Go to Messages', role: 'parent' }
    };

    let keySequence = '';
    let sequenceTimeout = null;
    let shortcutsEnabled = true;

    // Initialize keyboard shortcuts
    function init() {
        // Load preferences
        const saved = localStorage.getItem('keyboardShortcutsEnabled');
        shortcutsEnabled = saved === null ? true : saved === 'true';

        if (shortcutsEnabled) {
            document.addEventListener('keydown', handleKeyPress);
        }

        // Add shortcuts toggle to settings
        addShortcutsToggle();
    }

    // Handle key presses
    function handleKeyPress(e) {
        // Ignore if user is typing in input field
        if (e.target.matches('input, textarea, select, [contenteditable]')) {
            return;
        }

        const key = e.key.toLowerCase();

        // Handle modifier keys
        if (e.ctrlKey || e.metaKey || e.altKey) {
            return; // Let browser handle these
        }

        // Clear previous timeout
        if (sequenceTimeout) {
            clearTimeout(sequenceTimeout);
        }

        // Build key sequence
        if (key === 'escape') {
            keySequence = 'esc';
        } else {
            keySequence += key;
        }

        // Check for matching shortcut
        const shortcut = shortcuts[keySequence];

        if (shortcut) {
            // Check context/role requirements
            if (isShortcutAvailable(shortcut)) {
                e.preventDefault();
                shortcut.action();
                keySequence = '';
                return;
            }
        }

        // Reset sequence after 1.5 seconds
        sequenceTimeout = setTimeout(() => {
            keySequence = '';
        }, 1500);
    }

    // Check if shortcut is available in current context
    function isShortcutAvailable(shortcut) {
        // Check role requirement
        if (shortcut.role) {
            const userRole = document.body.dataset.userRole;
            if (userRole !== shortcut.role) {
                return false;
            }
        }

        // Check context requirement
        if (shortcut.context) {
            const currentContext = document.body.dataset.context;
            if (currentContext !== shortcut.context) {
                return false;
            }
        }

        return true;
    }

    // Navigation actions
    function goToDashboard() {
        const role = document.body.dataset.userRole || 'student';
        window.location.href = `/${role}/dashboard`;
    }

    function goToSubjects() {
        window.location.href = '/subjects';
    }

    function goToArcade() {
        window.location.href = '/arcade';
    }

    function goToTutorials() {
        window.location.href = '/tutorials';
    }

    function goToClasses() {
        window.location.href = '/teacher/classes';
    }

    function goToGradebook() {
        window.location.href = '/teacher/gradebook';
    }

    function createAssignment() {
        window.location.href = '/teacher/create-assignment';
    }

    function goToProgress() {
        window.location.href = '/parent/analytics';
    }

    function goToMessages() {
        const role = document.body.dataset.userRole || 'student';
        window.location.href = `/${role}/messages`;
    }

    // Assignment actions
    function nextQuestion() {
        const nextBtn = document.querySelector('[data-action="next-question"], .next-btn, #nextBtn');
        if (nextBtn && !nextBtn.disabled) {
            nextBtn.click();
        }
    }

    function previousQuestion() {
        const prevBtn = document.querySelector('[data-action="prev-question"], .prev-btn, #prevBtn');
        if (prevBtn && !prevBtn.disabled) {
            prevBtn.click();
        }
    }

    function submitAnswer() {
        const submitBtn = document.querySelector('[data-action="submit"], .submit-btn, button[type="submit"]:not([form])');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
        }
    }

    function showHint() {
        const hintBtn = document.querySelector('[data-action="hint"], .hint-btn, #showHint');
        if (hintBtn) {
            hintBtn.click();
        }
    }

    // General actions
    function focusSearch() {
        const search = document.querySelector('#global-search, [type="search"], .search-input');
        if (search) {
            search.focus();
            search.select();
        }
    }

    function closeModal() {
        // Close any open modals/dialogs
        const modal = document.querySelector('.modal.show, [role="dialog"][open]');
        if (modal) {
            const closeBtn = modal.querySelector('.close, [data-dismiss="modal"]');
            if (closeBtn) {
                closeBtn.click();
            }
        }

        // Close any dropdowns
        const dropdown = document.querySelector('.dropdown.show');
        if (dropdown) {
            dropdown.classList.remove('show');
        }
    }

    function showShortcutHelp() {
        // Create shortcuts help modal
        const modal = createShortcutsModal();
        document.body.appendChild(modal);
        modal.style.display = 'block';
    }

    // Create shortcuts help modal
    function createShortcutsModal() {
        const modal = document.createElement('div');
        modal.className = 'keyboard-shortcuts-modal';
        modal.innerHTML = `
            <div class="shortcuts-modal-overlay" onclick="this.parentElement.remove()"></div>
            <div class="shortcuts-modal-content">
                <div class="shortcuts-modal-header">
                    <h2>⌨️ Keyboard Shortcuts</h2>
                    <button class="close-btn" onclick="this.closest('.keyboard-shortcuts-modal').remove()">×</button>
                </div>
                <div class="shortcuts-modal-body">
                    ${generateShortcutsList()}
                </div>
            </div>
        `;
        return modal;
    }

    // Generate shortcuts list HTML
    function generateShortcutsList() {
        const userRole = document.body.dataset.userRole;
        const context = document.body.dataset.context;

        const groups = {
            'Navigation': [],
            'Assignment': [],
            'General': [],
            'Teacher': [],
            'Parent': []
        };

        // Categorize shortcuts
        for (const [keys, shortcut] of Object.entries(shortcuts)) {
            // Skip if role doesn't match
            if (shortcut.role && shortcut.role !== userRole) continue;

            // Skip if context doesn't match
            if (shortcut.context && shortcut.context !== context) continue;

            const item = `
                <div class="shortcut-item">
                    <kbd>${keys.split(' ').map(k => k.toUpperCase()).join('</kbd> <kbd>')}</kbd>
                    <span>${shortcut.description}</span>
                </div>
            `;

            if (keys.startsWith('g ')) {
                groups['Navigation'].push(item);
            } else if (shortcut.context === 'assignment') {
                groups['Assignment'].push(item);
            } else if (shortcut.role === 'teacher') {
                groups['Teacher'].push(item);
            } else if (shortcut.role === 'parent') {
                groups['Parent'].push(item);
            } else {
                groups['General'].push(item);
            }
        }

        // Build HTML
        let html = '';
        for (const [group, items] of Object.entries(groups)) {
            if (items.length > 0) {
                html += `
                    <div class="shortcuts-group">
                        <h3>${group}</h3>
                        ${items.join('')}
                    </div>
                `;
            }
        }

        return html;
    }

    // Add shortcuts toggle to settings
    function addShortcutsToggle() {
        // This would be added to user settings page
        // For now, just provide a way to toggle via localStorage
    }

    // Public API
    window.KeyboardShortcuts = {
        enable: function() {
            shortcutsEnabled = true;
            localStorage.setItem('keyboardShortcutsEnabled', 'true');
            document.addEventListener('keydown', handleKeyPress);
        },
        disable: function() {
            shortcutsEnabled = false;
            localStorage.setItem('keyboardShortcutsEnabled', 'false');
            document.removeEventListener('keydown', handleKeyPress);
        },
        show: showShortcutHelp
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
