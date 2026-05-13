# SLIB Finder — API & Microservices Directory

> A centralized, searchable directory for discovering, managing, and comparing APIs and microservices. Built as a SENG 701 Software Engineering Capstone project at UMBC.

**Live App:** [https://slib-directory-finder.vercel.app](https://slib-directory-finder.vercel.app)  
**GitHub:** [https://github.com/Mounika2526/slib-directory-finder](https://github.com/Mounika2526/slib-directory-finder)

---

## What is SLIB Finder?

SLIB Finder helps software engineers, product owners, and developers discover and evaluate APIs and microservices from a centralized library. Instead of juggling spreadsheets or hunting across multiple tools, users can search, filter, compare, and analyze **300+ API entries** across 15 categories — all in one place.

---

## Features

- **Add / Edit / Delete** API entries via a slide-in form drawer
- **GitHub Auto-Fetch** — paste a GitHub repo URL to auto-fill entry fields, then review and complete before saving
- **Relevance-Ranked Fuzzy Search** — handles typos (e.g. "Stipe" finds "Stripe") using bigram scoring across name, description, language, category, developer, and more
- **Category Filter** — narrow results by API category (15 categories)
- **Sort Options** — 6 sort types: name A–Z, name Z–A, risk high/low, category, developer
- **Side-by-Side Comparison** — compare up to 4 APIs at once with colour-highlighted differences and a sticky toolbar
- **Stats Dashboard** — 8 charts (category breakdown, developer counts, risk levels, languages, cost distribution, design patterns, scalability, developer leaderboard) with filter controls
- **Sample Code Generation** — auto-generate starter code snippets in 11 languages: JavaScript, TypeScript, Python, Java, Go, Ruby, PHP, Rust, C#, Kotlin, Swift + cURL fallback
- **4-Column Card Grid** — expandable cards with full detail view and equal-height rows
- **Smart Pagination** — 12 cards per page with dots navigation (1 … 4 5 6 … 26)
- **Risk Level** — auto-calculated from version string (v0.x = High, stable = Low)
- **Empty Fields Indicator** — cards show ⚠ missing / ✓ complete status
- **CSV Export** — download the current filtered view as a CSV file
- **Shareable Card Links** — copy a direct link to any API card
- **Print View** — open a formatted print-ready view of any API entry
- **Back to Top** — floating button appears after scrolling 300px
- **300+ Database Entries** — across 15 categories and 230+ developers, auto-seeded on first deploy

---

## Tech Stack

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Frontend | React + Vite | Vercel |
| Backend | Flask (Python) | Render |
| Database | SQLite (dev) / PostgreSQL (prod) | Render |
| Styling | Tailwind CSS | — |

---

## Project Structure

```
slib-directory-finder/
├── backend/
│   ├── app.py              # Flask backend — REST API endpoints and database model
│   ├── seed_data.py        # Database seeder — 300+ API entries (runs once on deploy)
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   ├── favicon.svg
│   │   └── icons.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Charts.jsx       # SimpleBarChart, DonutChart, StatCard
│   │   │   ├── CompareModal.jsx # Side-by-side API comparison overlay
│   │   │   ├── ReviewModal.jsx  # Post-GitHub-fetch review form
│   │   │   └── StatsTab.jsx     # Analytics dashboard with filters
│   │   ├── utils/
│   │   │   ├── codeGenerator.js # Language-specific code snippet templates
│   │   │   ├── riskHelpers.js   # Risk badge and color utilities
│   │   │   └── search.js        # Bigram scoring and relevance ranking
│   │   ├── App.jsx              # Root component — state management and UI
│   │   ├── main.jsx             # React entry point
│   │   └── index.css            # Tailwind CSS import
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── .gitignore
├── runtime.txt              # Python version for Render
└── README.md
```

---

## Running Locally

### Prerequisites

- Python 3.13+
- Node.js 18+
- npm

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Mounika2526/slib-directory-finder.git
cd slib-directory-finder

# Install Python dependencies
pip install -r backend/requirements.txt

# Start the Flask backend (runs on port 5001)
cd backend
python app.py
```

### Frontend Setup

```bash
# From the project root
cd frontend

# Install Node dependencies
npm install

# Start the Vite dev server (runs on port 5173)
npm run dev
```

The app will be available at `http://localhost:5173`.

> **Note:** The frontend points to the production backend by default. To use your local backend, update the `API_BASE` constant in `frontend/src/App.jsx` to `http://localhost:5001`.

### Build for Production

```bash
cd frontend
npm run build
```

Output goes to the `dist/` folder and can be deployed to any static host.

---

## Deployment

### Frontend — Vercel

1. Connect your GitHub repo to [Vercel](https://vercel.com)
2. Set the **Root Directory** to `frontend`
3. Set the build command to `npm run build` and output directory to `dist`
4. Deploy — Vercel redeploys automatically on every push to `main`

### Backend — Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repo and set the **Root Directory** to `backend`
3. Set the start command to: `gunicorn app:app`
4. Add a **PostgreSQL** database and link it — Render provides `DATABASE_URL` automatically
5. Deploy

> **Note:** The backend runs on Render's free tier. After inactivity it may take up to 30 seconds to wake up on first load.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/test` | API connectivity test |
| GET | `/api/apis` | Retrieve all API entries |
| POST | `/api/apis` | Create a new API entry |
| PUT | `/api/apis/<id>` | Update an existing entry |
| DELETE | `/api/apis/<id>` | Delete an entry |
| POST | `/api/github-fetch` | Auto-fill entry from a GitHub repo |

---

## Database

The app uses **SQLite** locally and **PostgreSQL** on Render.

The `ApiEntry` model stores:

| Field | Type | Required |
|-------|------|----------|
| name | String | ✅ |
| category | String | ✅ |
| description | String | ✅ |
| version | String | ✅ |
| developer | String | ✅ |
| risk_level | String | auto-computed |
| programming_language | String | optional |
| framework | String | optional |
| cost | String | optional |
| latency | String | optional |
| scalability | String | optional |
| design_pattern | String | optional |
| sample_code | Text | optional |

Risk level is automatically derived from the version string:
- `v0.x` or `0.x.x` → **High** (pre-release / unstable)
- Empty / unknown → **Medium**
- All other versions → **Low** (stable release)

---

## Known Limitations

- **Cold start delay:** The backend runs on Render's free tier and may take 20–30 seconds to respond after a period of inactivity.
- **No authentication:** All entries are publicly readable and editable — designed for internal/team use.
- **SQLite in development:** Local dev uses SQLite; production uses PostgreSQL on Render. Schema is fully compatible across both.

---

## Student Information

| Field | Detail |
|-------|--------|
| Student | Mounika Dasari |
| Course | SENG 701 – Software Engineering Capstone |
| Institution | University of Maryland, Baltimore County (UMBC) |
| Advisor | Professor Mohammad Samarah / Professor Melissa |
| Sponsor | UMBC In-house Project |

---

## References

- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org)
- [Render Deployment Docs](https://render.com/docs)
- [Vercel Deployment Docs](https://vercel.com/docs)
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs/v4-beta)