# Vercel deployment

1. Import `shivesh2334-ai/cxr-learning-app-2` into your intended Vercel team.
2. Root directory: repository root. Framework: Other. Node.js: 24.x.
3. Build: `npm run build`. Output: `dist`. Install: `npm ci`.
4. Set server-only `GEMINI_API_KEY`. Optional: `GEMINI_MODEL`.
5. Deploy. Verify the learning library, manual report download and image preview.
6. Submit a de-identified radiograph to test Gemini. Verify the local observation-based fallback when the key or quota is unavailable. Test marker placement/removal and PNG/text downloads.

The `api/analyze.js` Node.js function is deployed separately from the static output. Do not select Streamlit or a Python build: Streamlit requires a persistent server and is not the Vercel entry point. There are no storage writes or database migrations.
