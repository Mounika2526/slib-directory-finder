# SBOM Finder (SLIB Directory Finder)

## Description
This project is part of my Software Engineering Capstone.

SBOM Finder is a full-stack web application that allows users to manage, search, and organize API and software component information. It provides a clean interface to perform CRUD operations and quickly locate relevant entries.

---

## Features
- Add new API entries
- View all APIs in a structured UI
- Edit existing API details
- Delete APIs
- Search and filter APIs in real time
- Responsive and modern UI using Tailwind CSS

---

## Tech Stack
Frontend:
- React (Vite)
- Tailwind CSS

Backend:
- Flask
- Flask-SQLAlchemy
- Flask-CORS

Database:
- SQLite

---

## Project Structure
project-root/
│
├── backend/
│   ├── app.py
│   ├── apis.db
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md

---

## Setup Instructions

### Backend Setup
cd backend  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python app.py  


### Frontend Setup
cd frontend  
npm install  
npm run dev  

Frontend runs at:  
http://localhost:5173  

---

## API Endpoints

GET /api/apis → Get all APIs  
POST /api/apis → Add new API  
PUT /api/apis/<id> → Update API  
DELETE /api/apis/<id> → Delete API  

---

## Current Status
- Full CRUD functionality implemented
- Search feature implemented
- UI enhanced with Tailwind CSS
- Backend and frontend fully integrated

---

## Future Enhancements
- SBOM file upload and parsing
- Advanced filtering (version, vendor, risk level)
- Authentication and user roles
- Deployment to cloud (Vercel + Render)
- PostgreSQL integration

---

## Author
Mounika Dasari