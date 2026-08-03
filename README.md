<<<<<<< HEAD
# Fashion Buddy — Build Log

An AI fashion recommendation app: upload a photo or type a query, get matching
clothing recommendations. Built with Claude for vision, Chroma for vector
search, and Tavily for web search — no low-code platform required.

## Phase 1: Vision module (you are here)

This lets Claude look at a photo and describe the clothing items in it, in a
clean structured format we'll use for search later.

### Setup

1. **Get an Anthropic API key**: https://console.anthropic.com/settings/keys

2. **Install Python 3.10+** if you don't have it already.

3. From the `backend/` folder, create a virtual environment and install deps:
   ```bash
   cd fashion-buddy/backend
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Set your API key as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...   # on Windows: set ANTHROPIC_API_KEY=sk-ant-...
   ```

5. Drop a test photo of an outfit into `fashion-buddy/data/test.jpg`

6. Run it:
   ```bash
   python vision.py
   ```

   You should see output like:
   ```
   TOPS - White cotton button-down shirt with a relaxed fit...
   BOTTOMS - High-waisted dark denim jeans with a straight leg...
   ```

### What's next (Phase 2)

Once this works, we'll:
- Build a small sample product catalog (or use a Kaggle fashion dataset)
- Embed it into a local Chroma vector database
- Take the description above and search the catalog for similar items

## Project structure so far
```
fashion-buddy/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── vision.py        ← Phase 1: image → clothing description
└── data/
    └── test.jpg          ← add your own test image here
```
=======
# fashionbuddy
Fashion AI Stylist and Clothing Recommendation
>>>>>>> 3bf51872ecfb584a4c6696623220606afab3512c
