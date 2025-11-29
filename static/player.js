// Web Player JavaScript
let currentPlaylist = [];
let currentTrackIndex = -1;
let isPlaying = false;
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const progressBar = document.getElementById('progressBar');
const volumeBar = document.getElementById('volumeBar');
const volumeValue = document.getElementById('volumeValue');
const trackTitle = document.getElementById('trackTitle');
const trackNumber = document.getElementById('trackNumber');
const currentTimeSpan = document.getElementById('currentTime');
const durationSpan = document.getElementById('duration');
const playlistDiv = document.getElementById('playlist');
const trackCountSpan = document.getElementById('trackCount');
const loadPlaylistBtn = document.getElementById('loadPlaylistBtn');
const refreshBtn = document.getElementById('refreshBtn');
const userTokenInput = document.getElementById('userTokenInput');

// Initialize volume
audioPlayer.volume = 1.0;

// Event listeners
playPauseBtn.addEventListener('click', togglePlayPause);
prevBtn.addEventListener('click', playPrevious);
nextBtn.addEventListener('click', playNext);
progressBar.addEventListener('input', seek);
volumeBar.addEventListener('input', changeVolume);
loadPlaylistBtn.addEventListener('click', loadPlaylist);
refreshBtn.addEventListener('click', () => {
    if (userTokenInput.value) {
        loadPlaylist();
    }
});

// Audio player events
audioPlayer.addEventListener('loadedmetadata', () => {
    durationSpan.textContent = formatTime(audioPlayer.duration);
    progressBar.max = audioPlayer.duration;
});

audioPlayer.addEventListener('timeupdate', () => {
    if (audioPlayer.duration) {
        progressBar.value = audioPlayer.currentTime;
        currentTimeSpan.textContent = formatTime(audioPlayer.currentTime);
    }
});

audioPlayer.addEventListener('ended', () => {
    playNext();
});

audioPlayer.addEventListener('error', (e) => {
    console.error('Audio error:', e);
    trackTitle.textContent = 'Error loading track';
    isPlaying = false;
    updatePlayPauseButton();
});

// Functions
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function togglePlayPause() {
    if (currentTrackIndex === -1 && currentPlaylist.length > 0) {
        playTrack(0);
        return;
    }
    
    if (isPlaying) {
        audioPlayer.pause();
        isPlaying = false;
    } else {
        audioPlayer.play();
        isPlaying = true;
    }
    updatePlayPauseButton();
}

function playTrack(index) {
    if (index < 0 || index >= currentPlaylist.length) return;
    
    currentTrackIndex = index;
    const track = currentPlaylist[index];
    audioPlayer.src = track;
    audioPlayer.load();
    audioPlayer.play();
    isPlaying = true;
    updatePlayPauseButton();
    updateTrackInfo();
    updatePlaylistUI();
}

function playPrevious() {
    if (currentPlaylist.length === 0) return;
    const newIndex = currentTrackIndex > 0 ? currentTrackIndex - 1 : currentPlaylist.length - 1;
    playTrack(newIndex);
}

function playNext() {
    if (currentPlaylist.length === 0) return;
    const newIndex = currentTrackIndex < currentPlaylist.length - 1 ? currentTrackIndex + 1 : 0;
    playTrack(newIndex);
}

function seek() {
    audioPlayer.currentTime = progressBar.value;
}

function changeVolume() {
    const volume = volumeBar.value / 100;
    audioPlayer.volume = volume;
    volumeValue.textContent = `${volumeBar.value}%`;
}

function updatePlayPauseButton() {
    playPauseBtn.textContent = isPlaying ? '⏸' : '▶';
}

function updateTrackInfo() {
    if (currentTrackIndex >= 0 && currentTrackIndex < currentPlaylist.length) {
        const track = currentPlaylist[currentTrackIndex];
        // Extract filename or URL for display
        const displayName = track.split('/').pop().split('?')[0] || track;
        trackTitle.textContent = displayName;
        trackNumber.textContent = `${currentTrackIndex + 1} / ${currentPlaylist.length}`;
    } else {
        trackTitle.textContent = 'No track selected';
        trackNumber.textContent = '-';
    }
}

function updatePlaylistUI() {
    playlistDiv.innerHTML = '';
    
    if (currentPlaylist.length === 0) {
        playlistDiv.innerHTML = '<div class="empty-state"><p>No tracks in playlist</p></div>';
        return;
    }
    
    currentPlaylist.forEach((track, index) => {
        const item = document.createElement('div');
        item.className = 'playlist-item';
        if (index === currentTrackIndex) {
            item.classList.add('active');
        }
        
        const displayName = track.split('/').pop().split('?')[0] || track;
        
        item.innerHTML = `
            <span class="playlist-item-number">${index + 1}</span>
            <span class="playlist-item-title">${displayName}</span>
        `;
        
        item.addEventListener('click', () => playTrack(index));
        playlistDiv.appendChild(item);
    });
}

async function loadPlaylist() {
    const token = userTokenInput.value.trim();
    if (!token) {
        alert('Please enter a user token');
        return;
    }
    
    try {
        loadPlaylistBtn.disabled = true;
        loadPlaylistBtn.textContent = 'Loading...';
        
        const response = await fetch(`/api/playlist?token=${encodeURIComponent(token)}`);
        const data = await response.json();
        
        if (data.success) {
            currentPlaylist = data.tracks;
            trackCountSpan.textContent = `${data.count} tracks`;
            updatePlaylistUI();
            
            if (currentPlaylist.length > 0) {
                // Auto-play first track
                playTrack(0);
            } else {
                playlistDiv.innerHTML = '<div class="empty-state"><p>No tracks found in playlist</p></div>';
            }
        } else {
            alert(`Error: ${data.error || 'Failed to load playlist'}`);
        }
    } catch (error) {
        console.error('Error loading playlist:', error);
        alert('Failed to load playlist. Please check your token and try again.');
    } finally {
        loadPlaylistBtn.disabled = false;
        loadPlaylistBtn.textContent = 'Load Playlist';
    }
}

// Check for token in URL
function getTokenFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('token');
}

// Initialize
const urlToken = getTokenFromURL();
if (urlToken) {
    userTokenInput.value = urlToken;
    loadPlaylist();
}
updatePlaylistUI();
updateTrackInfo();

