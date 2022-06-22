# Radio Coda Stream Utilities
The following repository contains the docker image for the scripts required to run the Radio Coda Stream.
All credit for the original scripts goes to [@ohld](https://github.com/ohld) and his article [How to create your 24/7 YouTube online radio](https://okhlopkov.medium.com/how-to-create-your-24-7-youtube-online-radio-ca9e6834c192)

Docker image and modifications made by [@ikifar2012](https://github.com/ikifar2012)

## Technical overview
The Docker image consists of two parts, the song title updater and ffmpeg.
The song title updater is a simple Python script that receives a webhook from [Azuracast] and updates the song title in a text file.
ffmpeg is responsible for taking the audio stream from [Azuracast] and compositing a gif along with the song title (read from the file outputted by the song title updater python script)
and streaming it all to YouTube.
The [s6-overlay] is used to ensure both processes are running at the same time in the same container.

[Azuracast]: https://github.com/AzuraCast/AzuraCast
[s6-overlay]: https://github.com/just-containers/s6-overlay