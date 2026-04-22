# SLIB Finder — API & Microservices Directory

> A centralized, searchable directory for discovering, managing, and comparing APIs and microservices. Built as a SENG 701 Software Engineering Capstone project at UMBC.

**Live App:** [https://slib-directory-finder.vercel.app](https://slib-directory-finder.vercel.app)  
**GitHub:** [https://github.com/Mounika2526/slib-directory-finder](https://github.com/Mounika2526/slib-directory-finder)

---

## What is SLIB Finder?

SLIB Finder helps software engineers, product owners, and developers discover and evaluate APIs and microservices from a centralized library. Instead of juggling spreadsheets or hunting across multiple tools, users can search, filter, compare, and analyze 138+ API entries — all in one place.

---

## Features

- **Add / Edit / Delete** API entries with a slide-in form drawer
- **GitHub Auto-Fetch** — paste a GitHub repo URL to auto-fill entry fields, then review before saving
- **Fuzzy Search** — handles typos (e.g. "Stipe" finds "Stripe") across name, description, language, category, and more
- **Category Filter** — narrow results by API category
- **Sort Options** — 6 sort types: name A–Z, name Z–A, risk high/low, category, developer
- **Side-by-Side Comparison** — compare up to 4 APIs at once with color-highlighted differences and a sticky toolbar
- **Stats Dashboard** — 6 charts (category breakdown, developer counts, risk levels, languages, cost distribution, design patterns) with filter controls
- **Sample Code Generation** — auto-generate starter code snippets in 11 languages: JavaScript, TypeScript, Python, Java, Go, Ruby, PHP, Rust, C#, Kotlin, Swift + cURL fallback
- **Compact 3-Column Card Grid** — expandable cards with full detail view
- **Pagination** — 12 cards per page
- **Risk Level** — auto-calculated from version string
- **Empty Fields Indicator** — cards show ⚠ missing / ✓ complete status
- **CSV Export** — download the current filtered view as a CSV file
- **Shareable Card Links** — copy a direct link to any API card
- **138 Database Entries** — auto-seeded on first deploy, never re-runs

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
├── app.py            # Flask backend — all REST API endpoints
├── seed_apis.py      # Database seeder — 138 API entries (runs once on deploy)
├── requirements.txt  # Python dependencies
├── src/
│   └── App.jsx       # React frontend — all UI components and state
├── index.html
├── vite.config.js
└── package.json
```

---

## Running Locally

### Prerequisites

- Python 3.x
- Node.js 18+
- npm

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/Mounika2526/slib-directory-finder.git
cd slib-directory-finder

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask backend (runs on port 5000 by default)
python app.py
```

### Frontend Setup

```bash
# Install Node dependencies
npm install

# Start the Vite dev server (runs on port 5173 by default)
npm run dev
```

The app will be available at `http://localhost:5173`. The frontend is configured to point to the production backend by default — update the `API_BASE` constant in `App.jsx` to `http://localhost:5000` when running locally.

### Build for Production

```bash
npm run build
```

Output goes to the `dist/` folder and can be deployed to any static host (Vercel, Netlify, etc.).

---

## Deployment

### Frontend — Vercel

1. Connect your GitHub repo to [Vercel](https://vercel.com)
2. Set the build command to `npm run build` and output directory to `dist`
3. Deploy — Vercel handles the rest automatically on every push

### Backend — Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repo
3. Set the start command to: `gunicorn app:app`
4. Add environment variable `DATABASE_URL` if using PostgreSQL (Render provides this automatically for linked databases)
5. Deploy

> **Note:** The backend is hosted on Render's **free tier**. After a period of inactivity, the server goes to sleep and takes up to 30 seconds to wake up on first load. A banner in the UI will notify users while the backend is starting up.

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
| POST | `/api/github-fetch` | Auto-fill entry from a GitHub repo URL |

---

## Known Limitations

- **Cold start delay:** The backend runs on Render's free tier and may take 20–30 seconds to respond after inactivity. A loading banner is shown in the UI during this time.
- **No authentication:** All entries are publicly readable and editable. 
- **SQLite in development:** Local dev uses SQLite; production uses PostgreSQL on Render. Schema is compatible across both.

---

## Student Information

| Field | Detail |
|-------|--------|
| Student | Mounika Dasari |
| Campus ID | JU70291 |
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
- [Render Deployment Docs](https://render.com/docs)
- [Vercel Deployment Docs](https://vercel.com/docs)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org)