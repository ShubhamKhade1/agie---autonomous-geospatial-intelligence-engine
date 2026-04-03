# AGIE (Kasukabe)

Welcome to the **AGIE**. This project is a comprehensive geospatial data handling and machine learning platform, designed for robust temporal modeling, ingestion of satellite APIs, and explainable AI. 

The application is built with a decoupled architecture, using a high-performance Python FastAPI backend, Celery task workers for distributed processing, and a modern React frontend framework (Vite + Tailwind CSS).

## 🚀 Features

- **Geospatial & Data Handling**: Powered by `geopandas`, `xarray`, `rasterio`, `shapely`, and Uber's `h3` indexing.
- **Data Ingestion**: Integrates with robust satellite APIs like `sentinelsat`, `copernicusmarine`, `earthaccess`, and `sentinelhub`.
- **Machine Learning & Time-Series**: Uses `scikit-learn`, `darts`, `pytorch-forecasting`, and `torch` for advanced temporal modeling.
- **Explainable AI (XAI)**: Understand model decisions contextually with `shap` and `lime`, enhanced with natural language explanations via `google-generativeai`.

## 🛠️ Technology Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework.
- [Celery](https://docs.celeryq.dev/) - Asynchronous task queue.
- [TimescaleDB](https://www.timescale.com/) (PostgreSQL 14) - Time-series optimization for spatial-temporal data.
- [Redis](https://redis.io/) - In-memory cache and message broker for Celery.

**Frontend:**
- [React](https://reactjs.org/) + [Vite](https://vitejs.dev/) - Fast frontend development.
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first styling.
- [Framer Motion](https://www.framer.com/motion/) - UI animations.
- [Leaflet](https://leafletjs.com/) & [Recharts](https://recharts.org/) - Geospatial rendering and data visualization.

---

## 🏗️ Local Development

The easiest way to initialize the core infrastructure (Database, Cache, API, and Workers) is by using Docker Compose.

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ 
- Node.js 18+

### 1. Setup Environment
Ensure your environment variables are configured.
```bash
cp .env.example .env
```

### 2. Run Backend Services (Docker Compose)
Start the database, redis, backend API, and background workers via docker-compose:
```bash
docker-compose up --build
```
- The backend API will be available at: `http://localhost:8000`
- API Documentation (SwaggerUI): `http://localhost:8000/docs`

### 3. Run the Frontend 
To run the React application locally, navigate to the `frontend/` directory and install dependencies:
```bash
cd frontend
npm install
npm run dev
```

---

## 📂 Project Structure

```text
Kasukabe/
├── docker-compose.yml   # Multi-container orchestration
├── requirements.txt     # Python backend dependencies
├── .env                 # Environment secrets
├── src/                 # Backend source code
│   ├── api/             # FastAPI controllers and routes
│   ├── engine/          # Core geospatial logic and models
│   ├── shared/          # Shared utilities
│   └── workers/         # Celery background tasks
├── frontend/            # Vite + React interface
├── config/              # Configuration files
├── data/                # Local data storage / ingestion drops
├── db/                  # Database migration scripts 
├── k8s/                 # Kubernetes deployment manifests
└── tests/               # Unit and integration tests
```

---

## 📜 License
*Add license information here.*
