#!/bin/bash

set -euo pipefail

log() {
  echo -e "\033[1;36m[DEPLOY]\033[0m $1"
}

log "Applying Kubernetes manifests..."

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

log "Deployment applied. Verifying rollout status..."
kubectl rollout status deployment azurekubelogger -n monitoring
