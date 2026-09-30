# 🥗 AI-Powered Personal Diet Planner with Cloud Storage

[![Cloud Computing](https://img.shields.io/badge/Cloud_Architecture-SaaS_%7C_PaaS_%7C_REST-blue.svg)](https://github.com/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Auth-JWT_%2B_PBKDF2-orange.svg)](https://jwt.io/)
[![Storage](https://img.shields.io/badge/Storage-Cloud_DB_%2B_Object_Store-purple.svg)](https://github.com/)
[![Tests](https://img.shields.io/badge/Tests-14%2F14_Passing-brightgreen.svg)](https://pytest.org/)

> **A comprehensive, cloud-native nutrition and wellness planning platform with automated metabolic BMR/TDEE calculation, AI meal plan synthesis, multi-tenant database isolation, and partitioned cloud object storage.**

---

## 📌 1. Project Overview & Problem Statement

### The Problem
- **Planning Fatigue:** Calculating daily caloric targets, BMR, and macronutrient ratios (Protein, Carbohydrates, Fats) manually is tedious, complex, and prone to user error.
- **Data Fragmentation:** Food logs and diet plans created on a desktop or phone remain trapped in local silos without centralized cloud synchronization.
- **Rigid Meal Plans:** Generic diets fail to account for dietary constraints (Vegetarian, Vegan, Non-Veg) and allergens (Nuts, Dairy, Gluten).
- **Unstructured File Storage:** Exported diet reports, meal photos, and nutrition PDFs require separate scalable object storage distinct from relational databases.

### The Solution: NutriCloud AI
A cloud-backed, full-stack application providing:
1. **Server-Side Metabolic Engine:** Accurate BMR and TDEE calculation via the **Mifflin-St Jeor formula**.
2. **AI Meal Recommendation Engine:** Multi-criteria knapsack optimization combined with cloud LLM connectors and automatic offline fallback for 100% uptime.
3. **Multi-Tenant Cloud Database:** Secure, isolated storage for user credentials, demographic metrics, and meal histories.
4. **Cloud Object Storage Hub:** Bucket-partitioned storage for downloading, uploading, and archiving exported meal plans and food logs.
5. **Zero-Trust Security:** Salted PBKDF2 password hashing and stateless JWT bearer token authentication.

---

## 🏛️ 2. Cloud Computing Concepts Demonstrated

| Concept | Implementation in this Project |
| :--- | :--- |
| **Software as a Service (SaaS)** | Complete end-user diet planning web application accessible via browser on any device. |
| **Platform as a Service (PaaS)** | Fully containerizable with zero-config deployment on Google Cloud Run, Render, or Firebase. |
| **Cloud Database** | Structured storage for user accounts, demographic metrics, and saved plans (`SQLite` simulation / `Firestore`). |
| **Cloud Object Storage** | Partitioned binary storage (`storage_bucket/{user_id}/`) for exported diet PDFs, text logs, and meal photos. |
| **Stateless REST API** | Stateless client-server architecture using standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`). |
| **Stateless Authentication (JWT)** | Signed JSON Web Tokens eliminating server session state to support horizontal auto-scaling. |
| **Multi-Tenant Data Isolation** | Cryptographic token extraction ensuring User A can never query or delete User B's records. |
| **Fault Tolerance & Resilience** | Heuristic fallback mechanism instantly engaging if external cloud AI APIs experience outages. |

---

## 📐 3. System Architecture

```
                         [ CLIENT LAYER ]
               Responsive Web Browser / Mobile App
                                │
                      (HTTPS / JWT Bearer)
                                ▼
                      [ APPLICATION LAYER ]
             Stateless Python REST API Server (app.py)
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   [ Auth Service ]       [ AI Engine ]       [ Cloud Gateway ]
   - PBKDF2 Hashing       - Mifflin-St Jeor   - DB Controller
   - JWT Verifier         - Knapsack Heuristic - Storage Controller
   - Token Lifecycle      - LLM Fallback              │
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
                         [ DATA LAYER ]
             ┌──────────────────┴──────────────────┐
             ▼                                     ▼
   [ Cloud Database ]                    [ Cloud Object Storage ]
  - User Profiles (BMR/TDEE)            - Partitioned Buckets
  - Goal Multipliers                    - Exported Plans (.txt / .json)
  - Saved Meal Catalog                  - Uploaded Food Diaries
```

---

## ⚡ 4. AI Recommendation Engine & Metabolic Formulas

### Metabolic Calculation (Mifflin-St Jeor)
- **Men:** $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} + 5$
- **Women:** $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} - 161$
- **Total Daily Energy Expenditure (TDEE):** $\text{TDEE} = \text{BMR} \times \text{Physical Activity Multiplier}$

### Goal Caloric Modifiers
- **Weight Loss / Deficit:** $-18\%$ calories (30% Protein / 40% Carbs / 30% Fat)
- **Muscle Gain / Surplus:** $+15\%$ calories (25% Protein / 50% Carbs / 25% Fat)
- **Maintenance:** $0\%$ delta (25% Protein / 45% Carbs / 30% Fat)
- **Fitness / High Protein:** $+5\%$ calories (35% Protein / 40% Carbs / 25% Fat)

---

## 📂 5. Project Folder Structure

```
AI-Powered-Personal-Diet-Planner-Cloud/
│
├── frontend/                     # Modern Single Page Application
│   ├── index.html                # Responsive Glassmorphism UI
│   └── src/
│       ├── app.js                # State controller & API client
│       └── style.css             # Polished CSS design system
│
├── backend/                      # Python REST API & Microservices
│   ├── app.py                    # REST API server & static file host
│   ├── services/
│   │   ├── auth_service.py       # Salted PBKDF2 & JWT security
│   │   └── tdee_service.py       # BMR/TDEE metabolic pipeline
│   └── utils/
│       └── helpers.py            # Response standardizers & sanitizers
│
├── ai_engine/                    # AI Diet Optimization Engine
│   ├── diet_engine.py            # Knapsack heuristic + LLM connector
│   └── food_data.json            # Curated 80+ item nutritional dataset
│
├── cloud/                        # Cloud Storage & Database Layer
│   ├── database_service.py       # Multi-tenant cloud DB abstraction
│   └── storage_service.py        # Cloud object storage bucket manager
│
├── tests/                        # Automated Test Suite (14 Tests)
│   ├── test_auth.py              # Password hashing & JWT tests
│   ├── test_diet_engine.py       # BMR, TDEE, and AI meal tests
│   ├── test_storage_service.py   # Cloud object storage tests
│   └── test_user_isolation.py    # Multi-tenant security tests
│
├── sample_data/                  # Demo users, logs, and sample data
├── docs/                         # Comprehensive Academic Documentation
│   ├── PROJECT_REPORT.md         # 23-section semester project report
│   ├── TEST_CASES.md             # Detailed test matrix table
│   ├── INTERVIEW_QA.md           # Top 10 predicted interview Q&As
│   ├── RESUME_BULLETS.md         # Placement resume bullet points
│   └── GITHUB_GUIDE.md           # 12-day Git commit proof strategy
│
├── requirements.txt              # Dependency specification
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git tracking rules
├── run_local.py                  # One-click launcher & demo seeder
└── README.md                     # Project documentation
```

---

## 🚀 6. Quick Local Setup & Execution

### Prerequisites
- Python 3.10 or higher.
- Zero mandatory external packages required for local execution!

### Step-by-Step Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Powered-Personal-Diet-Planner-Cloud.git
   cd AI-Powered-Personal-Diet-Planner-Cloud
   ```

2. **Run with One Click:**
   ```bash
   python run_local.py
   # Or on Windows with python launcher:
   py run_local.py
   ```

3. **Access the Application:**
   - Web Browser will open automatically at: **`http://localhost:8000`**
   - **Default Demo Account:**
     - **Email:** `demo@cloudhealth.org`
     - **Password:** `DemoPass123`

---

## 🧪 7. Automated Test Suite

Execute the automated test suite verifying all 14 security, metabolic, and storage scenarios:

```bash
# Run tests with built-in runner:
py -m unittest discover tests

# Or with pytest (if installed):
pytest tests/
```

**Output:**
```
..............
----------------------------------------------------------------------
Ran 14 tests in 0.252s

OK
```

---

## 🌐 8. Cloud Deployment Guide

### Option A: Free-Tier Containerized Deployment (Google Cloud Run / Render)
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   ENV PORT=8080
   CMD ["python", "backend/app.py"]
   ```
2. Deploy via Google Cloud Run:
   ```bash
   gcloud run deploy diet-planner-cloud --source . --port 8080 --allow-unauthenticated
   ```

### Option B: Firebase Full-Stack Architecture
- **Frontend:** Firebase Hosting (`firebase deploy --only hosting`)
- **Backend / AI:** Firebase Cloud Functions / Cloud Run
- **Database:** Cloud Firestore (`/users/{uid}/profile`, `/users/{uid}/plans`)
- **Storage:** Firebase Cloud Storage (`gs://your-bucket/{uid}/`)

---

## 🛡️ 9. Security & Multi-Tenancy

- **Password Encryption:** Passwords hashed with 100,000 iterations of PBKDF2-HMAC-SHA256 and unique 16-byte random salts.
- **Tenant Isolation:** Enforced on all queries via parameter binding (`WHERE user_id = ?`).
- **Object Storage Whitelisting:** Strict extension filters (`.pdf`, `.txt`, `.jpg`, `.png`, `.json`) and maximum size caps (10MB) prevent malicious payload uploads.

---

## 💡 10. Placement & Interview Highlights

- **"Explain your project":** Discussed as a dual-tier cloud application solving nutrition adherence through automated BMR/TDEE calculation, AI meal synthesis with offline fallback, and partitioned object storage archiving.
- **Resume Ready:** Includes 3 tailored bullet points, a 2-line summary, and a LinkedIn showcase post inside [`docs/RESUME_BULLETS.md`](docs/RESUME_BULLETS.md).

---

## ⚠️ Disclaimer
*This project is an academic simulation created for Cloud Computing demonstration. Diet plans and caloric targets are general wellness suggestions and do not constitute clinical or medical nutrition advice.*

---

## 👨‍💻 Author
- **Course:** Cloud Computing Project Portfolio
- **Status:** Complete, Tested, and Placement-Ready.
