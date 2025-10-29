# Google Drive Setup for Colab

## For This Project: You Don't Need It!

The notebooks work perfectly without Google Drive. Everything runs locally in Colab's file system.

**Skip this section unless you specifically want to save outputs to Drive.**

## If You Want to Use Google Drive (Optional)

### Option 1: Simple Mount (Recommended)

Just add this at the start of your notebook:

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Now you can access your Drive
# e.g., '/content/drive/MyDrive/LawBot'
```

That's it! No OAuth2 setup needed.

### Option 2: Save Outputs to Drive (Optional)

If you want to save model weights, datasets, etc. to Drive:

```python
# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Create project directory in Drive
import os
os.makedirs('/content/drive/MyDrive/LawBot', exist_ok=True)

# Update paths in notebooks to use Drive instead of local
# Example:
# OLD: '../data/processed/'
# NEW: '/content/drive/MyDrive/LawBot/data/processed/'
```

### Option 3: Use OAuth2 with Client ID/Secret (Advanced)

Only if you need programmatic access via API:

```python
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LoadCredentialsFile("creds.json")

if gauth.credentials is None:
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("creds.json")
drive = GoogleDrive(gauth)
```

**You'll need to set up OAuth2 credentials:**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID
3. Download credentials.json (should look like this):

```json
{
  "installed": {
    "client_id": "your_client_id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_client_secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

4. Upload credentials.json to Colab
5. Use in notebooks

## For This Assignment

**Just use Option 1** - it's the easiest and sufficient for all requirements:

```python
# Add to top of notebooks that need Drive
from google.colab import drive
drive.mount('/content/drive')
```

## Summary

| Method | Complexity | Good For |
|--------|-----------|----------|
| Simple Mount | ⭐ Easy | Saving outputs |
| OAuth2 Client | ⭐⭐⭐ Complex | Programmatic access |

**Recommendation:** Use simple mount if you need Drive at all. Otherwise, skip Drive entirely - the notebooks work fine without it!

