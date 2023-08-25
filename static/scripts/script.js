document.addEventListener("DOMContentLoaded", () => {
    const instructionElement = document.getElementById("instruction");
    const startButton = document.getElementById("start");
    const pauseButton = document.getElementById("pause");
    const resumeButton = document.getElementById("resume");
    const stopButton = document.getElementById("stop");
    const playMusicButton = document.getElementById("play-music");
    const stopMusicButton = document.getElementById("stop-music");

    let musicPlaying = false;

    const toggleMusicButtons = () => {
        playMusicButton.disabled = musicPlaying;
        stopMusicButton.disabled = !musicPlaying;
    };

    playMusicButton.addEventListener("click", () => {
        fetch('/play_music', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    musicPlaying = true;
                    toggleMusicButtons();
                }
            });
    });

    stopMusicButton.addEventListener("click", () => {
        fetch('/stop_music', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    musicPlaying = false;
                    toggleMusicButtons();
                }
            });
    });

    startButton.addEventListener("click", () => {
        fetch('/start_session', { method: 'POST' });
    });

    pauseButton.addEventListener("click", () => {
        fetch('/pause_session', { method: 'POST' });
    });

    resumeButton.addEventListener("click", () => {
        fetch('/resume_session', { method: 'POST' });
    });

    stopButton.addEventListener("click", () => {
        fetch('/stop_session', { method: 'POST' });
    });
});
