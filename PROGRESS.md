# BookTalk — Plan de suivi projet

> **Comment utiliser ce fichier** : Ouvre ce fichier à chaque session Claude et colle son contenu dans le chat. Claude reprendra exactement où tu t'es arrêtée.

---

## Contexte profil

- **Nom** : Ghizlane Zahir
- **Profil** : Platform Engineer / DevOps — GCP + Azure + AWS
- **TJM actuel** : 630€ → objectif 800–900€
- **Certifications** : Terraform Associate (2021), GCP Solutions Architect (2020), LPIC-1
- **Maîtrisé** : Terraform, Ansible, Jenkins, GitLab CI, Docker, GCP, Azure, Python intermédiaire
- **À apprendre via ce projet** : Kubernetes (GKE), Claude API, FastAPI, Helm, CI/CD avancé
- **Objectif du projet** : Apprendre K8s + IA en construisant une vraie app → CV + side project

---

## Le projet : BookTalk

Une app vocale IA qui lit les livres à ta place.
- Tu uploades un PDF ou donnes un titre
- Tu poses des questions à voix haute
- L'app te répond avec une voix naturelle

---

## Architecture technique

```
┌─────────────────────────────────────────────────────┐
│                    UTILISATEUR                       │
│              (navigateur — micro + haut-parleur)     │
└─────────────────────┬───────────────────────────────┘
                      │ Web Speech API (voix → texte)
                      ▼
┌─────────────────────────────────────────────────────┐
│                 FRONTEND                             │
│              React + Web Speech API                  │
│   - Upload PDF/titre                                 │
│   - Capture voix → texte                            │
│   - Joue la réponse audio                           │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP REST
                      ▼
┌─────────────────────────────────────────────────────┐
│                 BACKEND (FastAPI)                    │
│                                                     │
│  ┌─────────────┐   ┌──────────────┐                │
│  │ /upload     │   │ /ask         │                │
│  │ Parse PDF   │   │ Question →   │                │
│  │ Stocke GCS  │   │ Claude API   │                │
│  └─────────────┘   └──────┬───────┘                │
│                           │                         │
│  ┌────────────────────────▼──────────────────────┐ │
│  │              Claude API (Anthropic)            │ │
│  │   Analyse livre + génère réponse intelligente  │ │
│  └────────────────────────┬──────────────────────┘ │
│                           │                         │
│  ┌────────────────────────▼──────────────────────┐ │
│  │         ElevenLabs / Google TTS API            │ │
│  │         Texte → audio naturel                  │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌──────────────────┐   ┌──────────────────────┐
│   PostgreSQL     │   │   Google Cloud       │
│   (metadata      │   │   Storage (GCS)      │
│    livres,       │   │   Fichiers PDF       │
│    historique)   │   │   + audio cache      │
└──────────────────┘   └──────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INFRASTRUCTURE (ce que tu apprends)

┌─────────────────────────────────────────────────────┐
│              GKE (Google Kubernetes Engine)          │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐               │
│  │  Pod         │  │  Pod         │               │
│  │  frontend    │  │  backend     │               │
│  │  (React)     │  │  (FastAPI)   │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  Ingress Controller (routing HTTP)           │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │  Helm Chart (packaging de toute l'app)       │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │ provisionné par
                       ▼
┌─────────────────────────────────────────────────────┐
│           Terraform (que tu maîtrises déjà)          │
│   - Crée le cluster GKE                             │
│   - Crée le bucket GCS                              │
│   - Configure IAM                                   │
└─────────────────────────────────────────────────────┘
                       │ déployé via
                       ▼
┌─────────────────────────────────────────────────────┐
│        GitHub Actions (CI/CD pipeline)               │
│   Push code → Tests → Build Docker → Deploy GKE     │
└─────────────────────────────────────────────────────┘
```

---

## Structure des fichiers du projet

```
booktalk/
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Interface principale
│   │   ├── components/
│   │   │   ├── BookUpload.jsx   # Upload PDF
│   │   │   ├── VoiceInput.jsx   # Capture micro
│   │   │   └── AudioPlayer.jsx  # Lecture réponse
│   └── Dockerfile
│
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── services/
│   │   ├── pdf_parser.py        # Extraction texte PDF
│   │   ├── claude_service.py    # Appels Claude API
│   │   └── tts_service.py       # Text-to-speech
│   ├── requirements.txt
│   └── Dockerfile
│
├── infra/                       # Terraform
│   ├── main.tf                  # GKE cluster + GCS
│   ├── variables.tf
│   └── outputs.tf
│
├── helm/                        # Kubernetes packaging
│   └── booktalk/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
│
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
│
├── PROGRESS.md                  ← CE FICHIER
└── README.md
```

---

## Plan semaine par semaine

### PHASE 1 — MVP local (semaines 1–3)
**Objectif : l'app fonctionne sur ton ordi**

| Semaine | Tâches | Ce que tu apprends |
|---------|--------|--------------------|
| Sem 1 | Installer Python, VS Code, créer le projet GitHub, FastAPI hello world | FastAPI, structure projet Python |
| Sem 2 | Upload PDF + extraction texte + appel Claude API | Claude API, parsing PDF, appels HTTP |
| Sem 3 | Ajout réponse vocale (TTS) + interface React basique | Web Speech API, React simple, intégration frontend/backend |

**Checkpoint Phase 1** : Tu poses une question sur un livre en texte → tu reçois une réponse vocale ✓

---

### PHASE 2 — Containeriser + déployer sur GKE (semaines 4–7)
**Objectif : l'app tourne sur Kubernetes dans le cloud**

| Semaine | Tâches | Ce que tu apprends |
|---------|--------|--------------------|
| Sem 4 | Dockerfile frontend + backend, docker-compose local | Docker multi-container, networking |
| Sem 5 | Terraform → créer cluster GKE + bucket GCS | GKE, Terraform que tu connais sur nouveau use case |
| Sem 6 | Premiers manifests K8s (Deployment, Service, Ingress) | K8s core concepts en conditions réelles |
| Sem 7 | Helm chart — packager toute l'app | Helm, templating K8s |

**Checkpoint Phase 2** : L'app est accessible via une URL publique sur GKE ✓

---

### PHASE 3 — Polish + CI/CD + monitoring (semaines 8–12)
**Objectif : projet pro prêt pour le CV et GitHub public**

| Semaine | Tâches | Ce que tu apprends |
|---------|--------|--------------------|
| Sem 8 | Micro vocal (Web Speech API) + modes intelligents (quiz, résumé, ELI5) | UX vocale, prompt engineering |
| Sem 9 | GitHub Actions — pipeline CI/CD complet | CI/CD avancé, automatisation deploy |
| Sem 10 | PostgreSQL sur K8s + historique des questions | StatefulSets K8s, bases de données |
| Sem 11 | Monitoring Grafana + alerting | Observabilité, un must sur le CV |
| Sem 12 | README pro + démo vidéo + LinkedIn post | Valorisation projet, personal branding |

**Checkpoint Phase 3** : Projet public sur GitHub avec README, démo, pipeline CI/CD ✓

---

## Progression

### Phase 1
- [ ] Semaine 1 — Setup + FastAPI hello world
- [ ] Semaine 2 — Upload PDF + Claude API
- [ ] Semaine 3 — Réponse vocale + React

### Phase 2
- [ ] Semaine 4 — Docker
- [ ] Semaine 5 — Terraform + GKE
- [ ] Semaine 6 — K8s manifests
- [ ] Semaine 7 — Helm

### Phase 3
- [ ] Semaine 8 — Voix + modes IA
- [ ] Semaine 9 — CI/CD
- [ ] Semaine 10 — PostgreSQL
- [ ] Semaine 11 — Monitoring
- [ ] Semaine 12 — Publication

---

## Journal de bord

<!-- Ajoute une ligne ici à chaque session -->
<!-- Format : ### DATE — Ce que j'ai fait / Ce qui bloque -->

---

## Rappels quotidiens suggérés (à mettre dans ton calendrier)

- **Lundi–Vendredi soir (30 min)** : coder ou lire sur la tâche de la semaine
- **Samedi (2h)** : session principale — avancer sur la semaine
- **Dimanche (15 min)** : noter ce qui bloque, préparer la semaine suivante

---

## Pour reprendre une session avec Claude

Copie-colle ce bloc au début de chaque conversation :

```
Bonjour, je travaille sur BookTalk (app vocale IA qui lit les livres).
Voici mon PROGRESS.md : [colle le contenu ici]
Aujourd'hui je veux : [ce que tu veux faire]
Voici ce qui bloque : [optionnel]
```

---

## Ressources clés

- Claude API : https://docs.anthropic.com
- FastAPI : https://fastapi.tiangolo.com
- GKE : https://cloud.google.com/kubernetes-engine
- Helm : https://helm.sh/docs
- ElevenLabs TTS : https://elevenlabs.io/docs
