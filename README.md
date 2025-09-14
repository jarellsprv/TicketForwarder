# TicketForwarder

A Python script to forward filtered emails into Google Docs and share them as commentable documents.

---

## Requirements

- Python 3.x
- IMAP-enabled Gmail account
- Google OAuth 2.0 Credentials
- Google Drive folder

---

## 1️⃣ OAuth 2.0 Credentials

This is the JSON file you get when you create credentials for your app in Google Cloud.

### Steps to get credentials:

1. Go to Google Cloud Console → APIs & Services → Credentials
2. Click **Create Credentials → OAuth client ID**
3. Choose **Desktop app**
4. Download the JSON file
5. Place it in your project under `data/input/` and set:

'GoogleDriveCredentailFileName' = "your-credentials-file-name"  (do not include .json)

---

## 2️⃣ Gmail App Password

To allow the script to log in and read emails, you need a Gmail App Password.

### Steps to generate a Gmail App Password:

1. Enable 2-Step Verification (if not already enabled):
   - Go to https://myaccount.google.com/security
   - Under "Signing in to Google", click **2-Step Verification → Turn on** and follow the prompts

2. Generate the App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Under "Select app", choose **Other (Custom name)** and type a name like "TicketForwarder"
   - Click **Generate**

3. Copy the generated password:
   - Google will give a 16-character password
   - Set in your config as: APP_PASSWORD = "the_generated_password"

---

## 3️⃣ Google Drive Folder ID (`GoogleDriveFolderId`)

### How to get the folder ID:

1. Open the folder in Google Drive
2. Look at the URL:

https://drive.google.com/drive/folders/<folder_id>

3. Copy `<folder_id>` and set it in your config: CONFIG["GoogleDriveFolderId"] = "<folder_id>"
