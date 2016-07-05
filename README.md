# html5-livestreaming

Requires https://github.com/dailymotion/hls.js/

There's a Flask route to serve static JS content from a subdirectory assumed to be named 'dist' containing either hls.js or hls.min.js, but any method of serving static content would work fine.

Set the `hostname` variable in `stream.py` to the appropriate value

Note: this is basically the python part of https://github.com/Nesseref/nginx-rtmp-auth plus a bit more Flask to template pages and load the JavaScript HLS player with the correct media location.
