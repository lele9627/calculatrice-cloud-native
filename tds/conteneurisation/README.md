# TD Conteneurisation

## 1) Frontend Nginx

**Fichiers** : `tds/conteneurisation/frontend/`

- `index.html` + `style.css`
- `Dockerfile` basé sur `nginx:latest`

### Point d'entrée
L'image Nginx démarre par défaut avec :
`nginx -g 'daemon off;'` (processus principal).

### Build & run
```bash
docker build . -t mon-frontend

docker run -d --name mon-frontend -p 8080:80 mon-frontend
```

### Modification du HTML
Observation attendue :
- Si l'image est **rebuild** puis le conteneur relancé, la nouvelle page est visible.
- Si on **redémarre** l'ancien conteneur sans rebuild, la page ne change pas.

## 2) Conteneur de debug (toolbox)

**Fichier** : `tds/conteneurisation/backend/Dockerfile`

- Base : `debian:latest`
- Paquets : `bash`, `htop`, `vim`, `net-tools`
- Variable `OWNER` définie
- Commande : `sleep 3600`

### Pourquoi pas d'EXPOSE ?
Le conteneur ne sert pas d'application réseau, il n'expose pas de port.

### Build
```bash
docker build . -t toolbox-ctn
```

### Exec
```bash
docker run -d --name toolbox toolbox-ctn

docker exec -it toolbox /bin/bash
```

### Curl depuis le conteneur
Observation attendue :
- `curl http://<IP-host>:8080` retourne le HTML du frontend
- Il faut utiliser l'IP de l'interface Docker du host

## 3) Gestion des droits

Avec `USER nonroot` :
- `whoami` retourne `nonroot`
- `apt install` échoue (pas de droits root)

**Conclusion** : l'utilisateur non root limite les opérations système dans le conteneur.

## 4) Registry GCP Artifact Registry

- Auth via `gcloud auth activate-service-account ...`
- Config docker : `gcloud auth configure-docker europe-west1-docker.pkg.dev`
- Tag attendu : `europe-west1-docker.pkg.dev/polytech-dijon/polytech-dijon/<image>:<tag>`

Exemple :
```
europe-west1-docker.pkg.dev/polytech-dijon/polytech-dijon/frontend-2026:nom1-nom2
```
