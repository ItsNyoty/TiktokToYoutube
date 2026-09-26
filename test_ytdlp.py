import yt_dlp

ydl_opts = {
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'writeinfojson': True,
    'impersonate': 'chrome',
    'playlistend': 1
}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.tiktok.com/@tiktok'])
    print("Success")
except Exception as e:
    print("Error:", e)
