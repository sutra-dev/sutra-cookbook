## 1. Product-Requirements Document (PRD)

*Project codename: “Global News Hub Web”*

### 1.1. Purpose & Vision

Create a lightweight, framework-free HTML/CSS/Vanilla JS front-end that mirrors the existing Streamlit prototype, but is deployable on any static host (GitHub Pages, Netlify, Vercel Static, etc.) and can be embedded in other sites or hybrid mobile shells. The UX should feel like a modern newsreader: fast, multilingual, accessible, and image-rich.

### 1.2. Target Users

* **General readers** looking for curated, translated world news.
* **Polyglots & language learners** who switch languages often.
* **Low-bandwidth users** on mobile devices (≤3 G connection).

### 1.3. Goals & Non-Goals

| Goals                                                                       | Non-Goals                                       |
| --------------------------------------------------------------------------- | ----------------------------------------------- |
| G1. Fetch news via Serper API.                                              | Building our own crawler.                       |
| G2. Translate content through Sutra LLM (REST endpoint).                    | Replacing or re-training the translation model. |
| G3. Provide language switcher with live re-render.                          | Account creation / user auth (v2).              |
| G4. Progressive enhancement → app works without JS (graceful degradation). | Server-side rendering; v1 is 100 % client-side. |
| G5. Responsive design (mobile-first).                                       | Native mobile app; PWA optional.                |

### 1.4. Functional Requirements

1. **Search bar** – debounced; Enter or click triggers fetch.
2. **Results list** – card layout: headline, source+date, snippet, “Read more” link, hero image (lazy-loaded).
3. **Language selector** – drop-down populated with the 52 supported languages; persists in `localStorage`.
4. **API-key modal** – one-time capture of Serper & Sutra keys, stored in `sessionStorage`; edit anytime.
5. **Pagination / “Load More”** – page param forwarded to Serper.
6. **Error handling** – human-readable notices for network/API failures.
7. **Accessibility** – WCAG 2.1 AA, ARIA roles, tab navigation, pref-ers-reduced-motion.

### 1.5. Non-Functional Requirements

* **Performance** : first contentful paint < 2 s on 3 G; bundle ≤ 150 kB gzip.
* **Security** : never log or transmit API keys to third-party domains.
* **i18n** : UI strings externalised in JSON.
* **Browser support** : last two versions of evergreen browsers + Safari 15.

### 1.6. Tech Stack

| Layer         | Choice                               | Rationale                  |
| ------------- | ------------------------------------ | -------------------------- |
| Mark-up       | Semantic HTML5                       | SEO, accessibility         |
| Styling       | CSS Modules + PostCSS (Autoprefixer) | Zero runtime; maintainable |
| Interactivity | Vanilla JS (ES2020) + Fetch API      | No framework overhead      |
| State         | Simple module pattern + Pub/Sub      | Small scope                |
| Tooling       | Vite (dev server & bundler)          | Fast HMR, tree-shaking     |
| QA            | Vitest + jsdom                       | Lightweight unit testing   |
| CI            | GitHub Actions                       | Auto-lint, build, deploy   |

### 1.7. User Flow

1. **First visit** → modal asks for keys.
2. Home shows default query “latest AI news” in English.
3. User types new query → press Enter → loading skeleton appears.
4. Data arrives → translate (if non-English) → render cards.
5. Language switcher → retranslate existing results client-side (no second Serper call).

### 1.8. Success Metrics

* Daily active users (DAU) > 1 k within 3 months.
* Average page-load CLS < 0.1.
* Translation latency (10 items) < 2 s  p95.
* Error-rate (5xx or model-fail) < 1 %.

### 1.9. Milestones & Timeline

| Week | Deliverable                                             |
| ---- | ------------------------------------------------------- |
| 1    | Wireframes, style guide, API contract docs.             |
| 2    | Core search & render flow, env-key modal, basic CSS.    |
| 3    | Translation integration, language switcher, pagination. |
| 4    | Accessibility pass, performance budget met, QA suite.   |
| 5    | Public beta, telemetry, docs, marketing site.           |

### 1.10. Risks & Mitigations

* **API-rate limits** → add local cache + exponential back-off.
* **Keys in frontend** → educate users; isolate in sessionStorage; advise proxy for production.
* **Large image payloads** → lazy-load, `srcset` for responsive sizes, WebP preferred.
