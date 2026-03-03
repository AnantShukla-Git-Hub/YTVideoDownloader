const API_URL = window.location.origin + '/api';

function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    showElement('error');
}

function showSuccess(message) {
    const successDiv = document.getElementById('success');
    successDiv.textContent = message;
    showElement('success');
}

async function fetchFormats() {
    const url = document.getElementById('videoUrl').value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL');
        return;
    }

    hideElement('error');
    hideElement('videoInfo');
    hideElement('success');
    showElement('loading');

    try {
        const response = await fetch(`${API_URL}/formats`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch video info');
        }
        
        document.getElementById('thumbnail').src = data.thumbnail;
        document.getElementById('videoTitle').textContent = data.title;
        
        const qualitySelect = document.getElementById('qualitySelect');
        qualitySelect.innerHTML = '';
        
        data.formats.forEach(format => {
            const option = document.createElement('option');
            option.value = format.format_id;
            option.textContent = `${format.quality} (${format.ext})`;
            qualitySelect.appendChild(option);
        });

        hideElement('loading');
        showElement('videoInfo');

    } catch (error) {
        hideElement('loading');
        showError(error.message);
    }
}

async function downloadVideo() {
    const url = document.getElementById('videoUrl').value.trim();
    const formatId = document.getElementById('qualitySelect').value;

    hideElement('error');
    hideElement('success');
    
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.disabled = true;
    downloadBtn.textContent = 'Downloading...';

    try {
        // Create a form and submit it to trigger download
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `${API_URL}/download`;
        form.style.display = 'none';
        
        const urlInput = document.createElement('input');
        urlInput.name = 'url';
        urlInput.value = url;
        form.appendChild(urlInput);
        
        const formatInput = document.createElement('input');
        formatInput.name = 'format_id';
        formatInput.value = formatId;
        form.appendChild(formatInput);
        
        document.body.appendChild(form);
        form.submit();
        
        // Show success message after a delay
        setTimeout(() => {
            showSuccess('Download started! Check your Downloads folder.');
            document.body.removeChild(form);
        }, 1000);

    } catch (error) {
        showError(error.message);
    } finally {
        setTimeout(() => {
            downloadBtn.disabled = false;
            downloadBtn.textContent = 'Download Video';
        }, 2000);
    }
}

document.getElementById('videoUrl').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchFormats();
    }
});
