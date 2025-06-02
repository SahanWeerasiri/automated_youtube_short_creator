document.getElementById('downloadButton').addEventListener('click', function () {
    const videoUrl = document.getElementById('videoUrl').value;
    if (videoUrl) {
        downloadVideo(videoUrl);
    } else {
        document.getElementById('errorMessage').textContent = 'Please enter a valid YouTube video URL.';
        document.getElementById('errorMessage').style.display = 'block';
    }
});

function downloadVideo(url) {
    // run the python script to download the video in cmd
    const command = `python youtube_downloader.py "${url}"`;
    const exec = require('child_process').exec;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            document.getElementById('errorMessage').textContent = 'An error occurred while trying to download the video.';
            document.getElementById('errorMessage').style.display = 'block';
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            document.getElementById('errorMessage').textContent = 'An error occurred while trying to download the video.';
            document.getElementById('errorMessage').style.display = 'block';
            return;
        }
        console.log(`stdout: ${stdout}`);
        document.getElementById('successMessage').textContent = 'Video downloaded successfully!';
        document.getElementById('successMessage').style.display = 'block';
    });
}