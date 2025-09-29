
# Brandskyddsbot â€“ Docker Compose

KÃ¶r en kÃ¤llaâ€‘lÃ¥st Streamlit-app bakom Nginx pÃ¥ port 80.
Appen blir tillgÃ¤nglig pÃ¥:  `http://<din-server>/brandskydd`

## Start
```bash
docker compose up -d --build
```

## Struktur
- `Dockerfile` â€“ bygger appcontainern
- `app.py` â€“ Streamlit-app (PDF â†’ RAG â†’ svar med kÃ¤llcitat)
- `requirements.txt`
- `.streamlit/config.toml` â€“ sÃ¤tter `baseUrlPath=brandskydd`
- `nginx/nginx.conf` â€“ reverse proxy till appen
- `docker-compose.yml` â€“ tvÃ¥ services (app, nginx)

## HTTPS (rekommenderas)
Placera bakom en omvÃ¤nd proxy med TLS (t.ex. din befintliga Nginx/Traefik) eller kÃ¶r nginxâ€‘proxyn pÃ¥ 443 med certifikat.

## BÃ¤dda in pÃ¥ din hemsida
```html
<iframe src="/brandskydd" style="width:100%;height:80vh;border:0"></iframe>
```
