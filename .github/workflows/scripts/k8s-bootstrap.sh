#!/bin/bash

set -euo pipefail

NAMESPACE="monitoring"
ACR_NAME="cogstakacr"

log() {
  echo -e "\033[1;34m[INFO]\033[0m $1"
}

error() {
  echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
}

log "Ensuring namespace '$NAMESPACE' exists..."
kubectl get namespace $NAMESPACE >/dev/null 2>&1 || kubectl create namespace $NAMESPACE

log "Creating ACR pull secret in '$NAMESPACE' namespace..."
kubectl get secret acr-secret -n $NAMESPACE >/dev/null 2>&1 || {
  ACR_USERNAME=$ACR_NAME
  ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

  kubectl create secret docker-registry acr-secret \
    --docker-server=$ACR_NAME.azurecr.io \
    --docker-username=$ACR_USERNAME \
    --docker-password="$ACR_PASSWORD" \
    --namespace=$NAMESPACE
}
