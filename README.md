# Virunga Intelligent Dashboard 🦍

## Architecture
This project replaces the legacy Google App Script system with a modern Python/Streamlit architecture.

### Components
1.  **Frontend**: Streamlit (Web App) - Responsive, Mobile-friendly.
2.  **Backend Logic**: Python (Pandas, Scikit-learn).
3.  **ML Engine**: 
    - **Clustering**: K-Means to segment activities by impact.
    - **NLP**: Sentiment analysis on press reviews (Mocked, ready for OpenAI API).
4.  **Data Source**: Google Sheets (via `gspread` - currently using Mock Data for demo).
5.  **Deployment**: Google Cloud Run (Dockerized).

## Local Setup (VS Code / Jupyter)
1.  Open this folder in VS Code.
2.  Open a terminal.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the app:
    ```bash
    streamlit run virunga_app.py
    ```
5.  The app will open in your browser.
6.  **Login**:
    - Email: `bbwende@virunga.org`
    - Password: `virunga2025`

## Deployment to Google Cloud Platform (GCP)
1.  Install Google Cloud SDK.
2.  Authenticate:
    ```bash
    gcloud auth login
    gcloud config set project [YOUR_PROJECT_ID]
    ```
3.  Build and Deploy:
    ```bash
    gcloud builds submit --tag gcr.io/[YOUR_PROJECT_ID]/virunga-dashboard
    gcloud run deploy virunga-dashboard --image gcr.io/[YOUR_PROJECT_ID]/virunga-dashboard --platform managed
    ```

## Features Implemented
- **Multi-Form Support**: Activities, Visitors, Press Review.
- **Security**: Role-based access (Owner vs Admin).
- **ML Analysis**: Automatic clustering of activities.
- **Design**: Premium Virunga color palette.
- **Actions**: Email reporting buttons.
