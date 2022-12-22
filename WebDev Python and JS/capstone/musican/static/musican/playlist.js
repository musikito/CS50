


// Create a WaveSurfer instance
var wavesurfer;

// Init on DOM ready
document.addEventListener('DOMContentLoaded', function () {
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#ddd',
        progressColor: '#ff006c',
        barWidth: 4,
        responsive: true,
        height: 90,
        barRadius: 4,
    });
});

// Bind controls
document.addEventListener('DOMContentLoaded', function () {
    /**
 * Formats time as HH:MM:SS
 * @param {number} seconds
 * @returns time as HH:MM:SS
 */
    const formatTimecode = seconds => {
        return new Date(seconds * 1000).toISOString().substr(11, 8)
    }

    const volumeBtn = document.getElementById("volumeBtn");
    const currentTime = document.getElementById("currentTime");
    // The playlist links
    let links = document.querySelectorAll('#playlist a');

    let currentTrack = 0;

    // Load a track by index and highlight the corresponding link
    let setCurrentSong = function (index) {
        links[currentTrack].classList.remove('active');
        currentTrack = index;
        links[currentTrack].classList.add('active');
        wavesurfer.load(links[currentTrack].href);
    };

    // Load the track on click
    Array.prototype.forEach.call(links, function (link, index) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            setCurrentSong(index);
        });
    });



    volumeBtn.onclick = function () {
        wavesurfer.toggleMute();
        if (volumeBtn.src.includes("volume.png")) {
            volumeBtn.src = "/static/musican/images/mute.png";
        } else {
            volumeBtn.src = "/static/musican/images/volume.png";
        }
    } // End of Volume button
    playBtn.onclick = function () {
        wavesurfer.playPause();
        // Change button img accordingly
        if (playBtn.src.includes("play.png")) {
            playBtn.src = "/static/musican/images/pause.png";
            playPause.innerHTML = '<i class="fa fa-pause"></i>';
        } else {
            playBtn.src = "/static/musican/images/play.png";
            playPause.innerHTML = '<i class="fa fa-play"></i>';
        } // End if
    } // End of play button

    stopBtn.onclick = function () {
        playBtn.src = "/static/musican/images/play.png";
        wavesurfer.stop();
    } // End of stop button


    // Play on audio load
    wavesurfer.on('ready', function () {
        wavesurfer.play();
        if (playBtn.src.includes("play.png")) {
            playBtn.src = "/static/musican/images/pause.png";
        }
        const duration = wavesurfer.getDuration()
        currentTime.innerHTML = formatTimecode(duration)

    });

    wavesurfer.on('error', function (e) {
        console.warn(e);
    });

    // Go to the next track on finish
    wavesurfer.on('finish', function () {
        setCurrentSong((currentTrack + 1) % links.length);
    });

    // Load the first track
    setCurrentSong(currentTrack);


});
