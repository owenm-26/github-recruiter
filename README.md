# github-recruiter
A new way to approach recruiting

## Architecture 
Backend: FastAPI
Frontend: Next.js

## How to Run
To run the backend install the relevant packages from `requirements.txt` and then launch the app from `./backend`

```bash
python -m venv venv
source venv/bin/activate
pip install requirements.txt -r
uvicorn main:app --reload
```

To run the frontend install the relevant packages and then run the app from `./frontend`
```bash
npm install
npm run dev
```