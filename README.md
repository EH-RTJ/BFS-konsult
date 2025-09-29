
# Brandskyddsbot – Docker Compose

Kör en källa‑låst Streamlit-app bakom Nginx på port 80.
Appen blir tillgänglig på:  `http://<din-server>/brandskydd`

## Start
```bash
docker compose up -d --build
```

## Struktur
- `Dockerfile` – bygger appcontainern
- `app.py` – Streamlit-app (PDF → RAG → svar med källcitat)
- `requirements.txt`
- `.streamlit/config.toml` – sätter `baseUrlPath=brandskydd`
- `nginx/nginx.conf` – reverse proxy till appen
- `docker-compose.yml` – två services (app, nginx)

## HTTPS (rekommenderas)
Placera bakom en omvänd proxy med TLS (t.ex. din befintliga Nginx/Traefik) eller kör nginx‑proxyn på 443 med certifikat.

## Bädda in på din hemsida
```html
<iframe src="/brandskydd" style="width:100%;height:80vh;border:0"></iframe>
```
