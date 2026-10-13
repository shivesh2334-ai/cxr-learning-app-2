# CXR Learning Studio

Vercel-ready chest radiograph education app with image preview, technical-quality review, systematic anatomy review, pattern analysis, AI report drafts, searchable learning references and manual report export. The original Streamlit modules are preserved under `app/` and `models/`; Vercel serves the web frontend and Node.js API instead of running Streamlit.

## Deploy on Vercel

Import this GitHub repository. Use the repository root, framework **Other**, Node.js **24.x**, build command `npm run build`, and output directory `dist`. `vercel.json` supplies these settings.

Add **GEMINI_API_KEY** as a server environment variable in Vercel. Optionally set **GEMINI_MODEL** (default `gemini-2.5-flash`). Never expose the key in frontend code. Redeploy after changing environment variables. No database is required.

Without a key, the learning library and manual reporting work; AI requests display a configuration message. Images are not stored by this app. AI analysis transmits uploaded images and context to Google Gemini; upload only de-identified material. Provider data policies apply.

## Local checks

```sh
npm ci
npm run build
npm test
```

Serve `dist/` with any static server to review the learning library and manual report. To run the API locally, use `vercel dev` with a local server environment variable.

## Scope

Educational drafts require qualified clinician review. The learning library is the existing repository JSON, not a trained image model or an image-based fallback. The repository has no bundled radiograph teaching images. The Python sources remain available for a separate Streamlit deployment; they are not executed on Vercel.
