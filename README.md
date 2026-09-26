# TikTok to YouTube Scheduler

This is a script that automatically downloads videos from a TikTok profile and schedules them as YouTube Shorts, 1 post per day at 9:30 AM.

## Step 1: Google Cloud Setup (YouTube API)
Because you are uploading videos via a script, YouTube requires you to create your own "App".

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your Google account (the one that manages your YouTube channel).
3. Click on **Select a project** in the top left and choose **New project**. Give it a name (e.g. "TikTokToYouTube") and click **Create**.
4. Make sure your new project is selected. In the search bar at the top, search for **YouTube Data API v3**. Click on it and press **Enable**.
5. In the left menu, go to **APIs & Services** > **OAuth consent screen**.
   - Choose **External** and click **Create**.
   - Fill in an App name (e.g. "Scheduler"), your email address in the required fields, and click Save at the bottom. (You can skip the Scopes page and just save/continue to the end).
   - IMPORTANT: Under **Test users**, you must add your own email address. If you don't do this, you will get an "Error 403: access_denied".
6. In the left menu, go to **Credentials**.
   - Click **Create credentials** and choose **OAuth client ID**.
   - Select Application type: **Desktop app**. Give it a name and click Create.
   - Click **DOWNLOAD JSON** (the download icon on the right).
7. Rename this downloaded file to exactly **`credentials.json`** and drag it into this project folder.

## Step 2: Running the script

Once you have placed `credentials.json` in the folder, you can start the script by typing this into your terminal:

```bash
.\venv\Scripts\python.exe main.py
```

1. The script will first ask for your TikTok username.
2. It will automatically download your videos.
3. Then it opens a webpage where you need to log in with your Google account and grant permission (Since it's your own app, Google might warn "Google hasn't verified this app". If so, click **Advanced** > **Go to [App name] (unsafe)**).
4. The script will then automatically upload and schedule your videos!
