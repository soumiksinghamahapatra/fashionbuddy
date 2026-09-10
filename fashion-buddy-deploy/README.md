# Fashion Buddy — Deploy to Render

This package deploys automatically using the included `render.yaml` —
Render reads it and sets up the whole service for you.

## Steps

1. **Upload this whole folder to a new GitHub repo**
   - Go to github.com → New repository → name it `fashion-buddy`
   - Click "uploading an existing file" and drag in everything from this folder
   - Commit

2. **Create a free Render account**
   - Go to render.com, sign up (you can sign up with your GitHub account
     directly, which makes step 3 easier)

3. **Create a new Blueprint**
   - On the Render dashboard, click **New +** → **Blueprint**
   - Connect your `fashion-buddy` GitHub repo
   - Render will detect `render.yaml` automatically and set up the build
     command, start command, and free plan for you

4. **Fill in your 3 secret keys when prompted**
   - `GOOGLE_API_KEY` — from aistudio.google.com
   - `TAVILY_API_KEY` — from tavily.com
   - `HF_TOKEN` — from huggingface.co/settings/tokens
   (Same keys you've already been using locally — you can copy them from
   your PowerShell setup, or generate fresh ones.)

5. **Click Deploy**
   - Render builds and starts the app automatically. After a few minutes
     you'll get a real public URL like `https://fashion-buddy-xxxx.onrender.com`

## Good to know

- **Free tier sleeps when idle.** If nobody visits for a while, the next
  visitor waits ~30-60 seconds for it to wake up. This is normal for free
  hosting, not a bug.
- **Redeploying:** any time you push new files to the GitHub repo, Render
  automatically rebuilds and redeploys — that's what "automatic deploy"
  means here.
- **Virtual try-on** still depends on the free public Hugging Face demo,
  same as when running locally — it can occasionally be slow or flaky.
