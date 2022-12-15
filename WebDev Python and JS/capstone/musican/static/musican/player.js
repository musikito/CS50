// Base url
const base_url = "/static/musican/images/";
// Song URL
const song_url = document.getElementById("song_url").getAttribute("data-src");
// Play Button
const playBtn = document.getElementById("playBtn");
// Stop Button
const stopBtn = document.getElementById("stopBtn");
// Like Button
const likeBtn = document.getElementById("likeBtn");
// Close Button
const closeBtn = document.getElementById("closeBtn");
// Volume Button
const volumeBtn = document.getElementById("volumeBtn");
// Time label
const currentTime = document.getElementById("currentTime");

/**
* Formats time as HH:MM:SS
* @param {number} seconds
* @returns time as HH:MM:SS
*/
const formatTimecode = seconds => {
    return new Date(seconds * 1000).toISOString().substr(11, 8)
}

var wavesurfer;
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

    wavesurfer.load(base_url + song_url);



    /*
    const wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#ddd',
        progressColor: '#ff006c',
        barWidth: 4,
        responsive: true,
        height: 90,
        barRadius: 4
    });
    */
    //wavesurfer.load(base_url + song_url);
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

    playBtn.onclick = function () {
        wavesurfer.playPause();
        // Change button img accordingly
        if (playBtn.src.includes("play.png")) {
            playBtn.src = "/static/musican/images/pause.png";
        } else {
            playBtn.src = "/static/musican/images/play.png";
        } // End if
    } // End of play button

    volumeBtn.onclick = function () {
        wavesurfer.toggleMute();
        if (volumeBtn.src.includes("volume.png")) {
            volumeBtn.src = "/static/musican/images/mute.png";
        } else {
            volumeBtn.src = "/static/musican/images/volume.png";
        }
    } // End of Volume button

    // Play on audio load
    wavesurfer.on('ready', function () {
        wavesurfer.play();
        if (playBtn.src.includes("play.png")) {
            playBtn.src = "/static/musican/images/pause.png";
        }

    }); // End of autoplay
    // Sets the timecode current timestamp as audio plays
    wavesurfer.on("audioprocess", () => {
        const time = wavesurfer.getCurrentTime()
        currentTime.innerHTML = formatTimecode(time)
    })
    stopBtn.onclick = function () {
        playBtn.src = "/static/musican/images/play.png";
        wavesurfer.stop();
        currentTime.innerHTML = "00:00:00"
    } // End of stop button

    closeBtn.onclick = function () {
        window.location = '/';
    } // End of closeBtn


    // Go to the next track on finish
    wavesurfer.on('finish', function () {
        playBtn.src = "/static/musican/images/play.png";
        setCurrentSong((currentTrack + 1) % links.length);
    });

    // Load the first track
    setCurrentSong(currentTrack);
});
