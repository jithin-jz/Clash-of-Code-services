# 🚢 AWS K3s Production Deployment

This directory contains the necessary Kubernetes manifests for running Clash of Code in a production environment.

## 📋 Prerequisites

- **K3s Cluster**: A running K3s cluster on AWS (e.g., on EC2).
- **kubectl**: CLI access to your cluster.
- **Traefik**: Standard K3s ingress controller.
- **cert-manager**: Installed for automatic SSL with Let's Encrypt.
- **Managed Services**: Ensure you have credentials for:
  - PostgreSQL (e.g., Supabase/RDS)
  - Redis (e.g., ElastiCache/Upstash)
  - Amazon DynamoDB
  - Cloudinary (Media hosting)
  - AWS SES (Transactional emails)

## 🔐 1. Configure Secrets

Do **not** store real secrets in this repository. Instead, create them directly in your cluster:

```bash
kubectl create secret generic coc-secrets -n coc \
  --from-literal=SECRET_KEY="your-django-secret" \
  --from-literal=DB_PASSWORD="your-db-password" \
  --from-literal=GOOGLE_CLIENT_ID="your-id" \
  --from-literal=GOOGLE_CLIENT_SECRET="your-secret" \
  --from-literal=CLOUDINARY_URL="your-cloudinary-url" \
  --from-literal=JWT_PRIVATE_KEY="$(cat your-private.pem)" \
  --from-literal=JWT_PUBLIC_KEY="$(cat your-public.pem)"
```

## ⚙️ 2. Configure Settings (ConfigMap)

Edit `configmaps.yaml` and update the following for your production environment:

- `FRONTEND_URL` & `BACKEND_URL`
- `DB_HOST`, `DB_PORT`, and `AWS_REGION`
- `EMAIL_BACKEND` (Set to SES or SMTP)

Set these frontend env vars in Vercel so the browser points at the ingress host:

- `VITE_API_URL=https://api.your-domain.com/api`
- `VITE_AI_URL=https://api.your-domain.com/ai`
- `VITE_CHAT_URL=wss://api.your-domain.com/ws/chat`
- `VITE_NOTIFICATIONS_WS_URL=wss://api.your-domain.com/ws/notifications`

## 🚀 3. Deploy

Apply the namespace first, then everything else:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f .
```

Run the database migrations:

```bash
kubectl apply -f migrate-job.yaml
```

## 🏥 4. Health Checks

Monitor the health of your services:

- **Core**: `https://api.your-domain.com/health/`
- **AI**: `https://api.your-domain.com/ai/health`
- **Chat WS**: `wss://api.your-domain.com/ws/chat/global`
- **Chat Health (cluster/internal)**: `http://chat:8001/`

## 🛠️ Update Workflow

When updating services:

1. Build and push new Docker images (e.g., `ghcr.io/your-user/coc-core:latest`).
2. Run `kubectl rollout restart deployment <service-name> -n coc`.
