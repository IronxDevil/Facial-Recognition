class FacialRecognitionApp {
    constructor() {
        this.isRecognitionActive = false;
        this.updateInterval = null;
        this.initializeElements();
        this.bindEvents();
        this.startResultsUpdater();
    }

    initializeElements() {
        // Buttons
        this.startBtn = document.getElementById('start-btn');
        this.stopBtn = document.getElementById('stop-btn');
        this.reloadBtn = document.getElementById('reload-btn');
        
        // Result elements
        this.identityElement = document.getElementById('identity');
        this.genderElement = document.getElementById('gender');
        this.emotionElement = document.getElementById('emotion');
        this.confidenceElement = document.getElementById('confidence');
        this.statusElement = document.getElementById('status');
        
        // Video feed
        this.videoFeed = document.getElementById('video-feed');
    }

    bindEvents() {
        this.startBtn.addEventListener('click', () => this.startRecognition());
        this.stopBtn.addEventListener('click', () => this.stopRecognition());
        this.reloadBtn.addEventListener('click', () => this.reloadDatabase());
        
        // Handle video feed errors
        this.videoFeed.addEventListener('error', () => {
            console.error('Video feed error');
            this.showNotification('Video feed error. Please check camera permissions.', 'error');
        });
    }

    async startRecognition() {
        try {
            this.setButtonLoading(this.startBtn, true);
            
            const response = await fetch('/start_recognition');
            const data = await response.json();
            
            if (response.ok) {
                this.isRecognitionActive = true;
                this.updateStatus('Active', true);
                this.startBtn.disabled = true;
                this.stopBtn.disabled = false;
                this.showNotification('Recognition started successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to start recognition');
            }
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.showNotification('Failed to start recognition: ' + error.message, 'error');
        } finally {
            this.setButtonLoading(this.startBtn, false);
        }
    }

    async stopRecognition() {
        try {
            this.setButtonLoading(this.stopBtn, true);
            
            const response = await fetch('/stop_recognition');
            const data = await response.json();
            
            if (response.ok) {
                this.isRecognitionActive = false;
                this.updateStatus('Inactive', false);
                this.startBtn.disabled = false;
                this.stopBtn.disabled = true;
                this.resetResults();
                this.showNotification('Recognition stopped successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to stop recognition');
            }
        } catch (error) {
            console.error('Error stopping recognition:', error);
            this.showNotification('Failed to stop recognition: ' + error.message, 'error');
        } finally {
            this.setButtonLoading(this.stopBtn, false);
        }
    }

    async reloadDatabase() {
        try {
            this.setButtonLoading(this.reloadBtn, true);
            
            const response = await fetch('/reload_database');
            const data = await response.json();
            
            if (response.ok) {
                this.showNotification(data.status, 'success');
            } else {
                throw new Error(data.error || 'Failed to reload database');
            }
        } catch (error) {
            console.error('Error reloading database:', error);
            this.showNotification('Failed to reload database: ' + error.message, 'error');
        } finally {
            this.setButtonLoading(this.reloadBtn, false);
        }
    }

    async updateResults() {
        if (!this.isRecognitionActive) return;
        
        try {
            const response = await fetch('/get_results');
            const data = await response.json();
            
            if (response.ok) {
                this.displayResults(data);
            }
        } catch (error) {
            console.error('Error fetching results:', error);
        }
    }

    displayResults(results) {
        // Update identity with color coding
        this.identityElement.textContent = results.identity;
        this.identityElement.className = 'value ' + (results.identity !== 'Unknown' ? 'recognized' : '');
        
        // Update gender
        this.genderElement.textContent = results.gender;
        
        // Update emotion with emoji
        const emotionEmojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'surprise': '😲',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐'
        };
        
        const emotionText = results.emotion;
        const emoji = emotionEmojis[emotionText.toLowerCase()] || '';
        this.emotionElement.textContent = `${emoji} ${emotionText}`;
        
        // Update confidence
        const confidence = results.confidence;
        this.confidenceElement.textContent = `${confidence}%`;
        this.confidenceElement.className = 'value ' + this.getConfidenceClass(confidence);
    }

    getConfidenceClass(confidence) {
        if (confidence >= 70) return 'high-confidence';
        if (confidence >= 40) return 'medium-confidence';
        return 'low-confidence';
    }

    resetResults() {
        this.identityElement.textContent = 'Unknown';
        this.identityElement.className = 'value';
        this.genderElement.textContent = 'Unknown';
        this.emotionElement.textContent = 'Unknown';
        this.confidenceElement.textContent = '0%';
        this.confidenceElement.className = 'value';
    }

    updateStatus(status, isActive) {
        this.statusElement.textContent = status;
        this.statusElement.className = `value ${isActive ? 'active' : 'inactive'}`;
        
        if (isActive) {
            this.statusElement.classList.add('pulse');
        } else {
            this.statusElement.classList.remove('pulse');
        }
    }

    setButtonLoading(button, isLoading) {
        if (isLoading) {
            button.innerHTML = '<span class="loading"></span> Loading...';
            button.disabled = true;
        } else {
            // Restore original text
            if (button === this.startBtn) {
                button.innerHTML = 'Start Recognition';
            } else if (button === this.stopBtn) {
                button.innerHTML = 'Stop Recognition';
            } else if (button === this.reloadBtn) {
                button.innerHTML = 'Reload Database';
            }
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="close-btn">&times;</button>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideIn 0.3s ease;
        `;
        
        // Set background color based on type
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            info: '#2196F3',
            warning: '#ff9800'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add close functionality
        const closeBtn = notification.querySelector('.close-btn');
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            margin-left: 10px;
        `;
        
        closeBtn.addEventListener('click', () => {
            notification.remove();
        });
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    startResultsUpdater() {
        // Update results every 500ms when recognition is active
        this.updateInterval = setInterval(() => {
            this.updateResults();
        }, 500);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .value.recognized {
        background: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb;
    }
    
    .value.high-confidence {
        background: #d4edda !important;
        color: #155724 !important;
    }
    
    .value.medium-confidence {
        background: #fff3cd !important;
        color: #856404 !important;
    }
    
    .value.low-confidence {
        background: #f8d7da !important;
        color: #721c24 !important;
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FacialRecognitionApp();
});