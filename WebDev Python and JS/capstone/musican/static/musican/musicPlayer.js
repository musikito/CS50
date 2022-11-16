// Play Button
var playBtn = document.getElementById("playBtn");

var wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#ddd',
    progressColor: '#ff006c',
    barWidth: 4,
    responsive: true,
    height: 90,
    barRadius: 4
});
wavesurfer.load("static/musican/images/songs/Son_MENTIRAS.mp3");

playBtn.onclick = function () {
    console.log("aqui");
    wavesurfer.playPause();
    // Change button img accordingly
    if (playBtn.src.includes("play.png")) {
        playBtn.src = "static/musican/images/pause.png";
    } else {
        playBtn.src = "static/musican/images/play.png";
    } // End if
} // End onclick

wavesurfer.on('finish', function () {
    playBtn.src = "static/musican/images/play.png";
    wavesurfer.stop();
})