# CXR Learning Studio

Vercel-ready chest radiograph education app with image preview, technical-quality review, systematic anatomy review, pattern analysis, AI report drafts, searchable learning references and manual report export. The original Streamlit modules are preserved under `app/` and `models/`; Vercel serves the web frontend and Node.js API instead of running Streamlit.

## Deploy on Vercel

Import this GitHub repository. Use the repository root, framework **Other**, Node.js **24.x**, build command `npm run build`, and output directory `dist`. `vercel.json` supplies these settings.

Add **GEMINI_API_KEY** as a server environment variable in Vercel. Optionally set **GEMINI_MODEL** (default `gemini-2.5-flash`). Never expose the key in frontend code. Redeploy after changing environment variables. No database is required.

Without a key (or when Gemini fails), reporting automatically uses a local retrieval-assisted draft based on clinician-entered observations. Select **Use local knowledge base only** to keep the image in the browser and avoid any API request. Images are not stored by this app. AI analysis transmits uploaded images and context to Google Gemini; upload only de-identified material. Provider data policies apply.

## Local checks

```sh
npm ci
npm run build
npm test
```

Serve `dist/` with any static server to review the learning library and manual report. To run the API locally, use `vercel dev` with a local server environment variable.

## Scope

Educational drafts require qualified clinician review. The original learning library is preserved. `public/reporting.js` adds seven source-linked teaching chunks with token-overlap retrieval and deterministic report composition. This is a lightweight RAG-style retrieval/template fallback, not vector embeddings or a local vision model. It cannot discover findings from uploaded pixels. No observations produces an explicit insufficient-information report; unmentioned structures are never presumed normal. The repository has no bundled radiograph teaching images. The Python sources remain available for a separate Streamlit deployment; they are not executed on Vercel.


## Uploaded X-ray reporting and annotation

1. Upload a de-identified JPEG, PNG or WebP under 2.5 MB.
2. Enter clinical context and visible findings, including side, zone and uncertainty. Choose structured reporting (default).
3. Analyze: with `GEMINI_API_KEY`, the existing Gemini REST integration requests a JSON report and approximate normalized annotation positions. With no key, quota/network errors or invalid model output, the same workflow returns a clearly labelled local draft using your observations and retrieved reference guidance.
4. Review and edit the report. Enter a finding label and click/tap its position on the original image to add a numbered marker; remove incorrect model markers. The app overlays graphics with canvas and does not synthesize X-ray anatomy.
5. Download the report text and annotated PNG with numbered findings and a preliminary-review footer. Exports are drafts, not signed reports.

Teaching chunks cover bullae/pneumothorax differentiation, consolidation, atelectasis, effusion, interstitial patterns and focal lesions. Source URLs are included in local reports. Retrieval relevance is text overlap, not diagnostic confidence; negated observations can still retrieve related teaching information, which remains separate from patient findings. Add reviewed chunks and sources in `public/reporting.js` to extend coverage. The original image from the chat is not bundled or used as a training example.

Automated tests cover input validation, missing keys, no-observation abstention, provider success/failure, malformed JSON, coordinate bounds and explicit local mode. Real provider inference needs a configured key and clinical validation; no diagnostic accuracy or localization performance has been established.

## Free-plan vision API: Groq

Create a free-plan API key at https://console.groq.com/keys and set **GROQ_API_KEY** as a server-only Vercel environment variable. Optional **GROQ_VISION_MODEL** defaults to `qwen/qwen3.8-27b`, listed in Groq's vision and free-plan limits documentation at implementation time. Redeploy after configuring it. Keep the account on the free plan if zero spend is required; the app cannot determine your provider billing tier or guarantee future pricing. Never paste keys into browser code or commit them.

Choose **Groq vision** to read uploaded pixels and draft a report/approximate numbered findings. **Auto** uses Gemini when its key is configured, otherwise Groq. An explicitly selected provider never silently forwards the image to another provider. Provider errors, 429 quota responses, timeouts or malformed output return the local observation-based draft. Local-only mode avoids both cloud providers entirely.

Groq receives the uploaded image and supplied clinical context. Use de-identified teaching material and review provider data terms. This is a general vision model, not a validated CXR diagnostic model. Free-plan quotas vary by account/model; consult https://console.groq.com/docs/rate-limits and https://console.groq.com/docs/vision. A free-plan key is still required; there is no anonymous image-reading service bundled with the app.
