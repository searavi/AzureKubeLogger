#!/bin/bash

# ------------------------
# Configurable Variables
# ------------------------
RESOURCE_GROUP="cogstak-realtime-services"
ACR_NAME="cogstakacr"
AKS_CLUSTER_NAME="cogstak-aks-cluster"
LOCATION="westus2"
NODE_COUNT=2

# ------------------------
# Utility Functions
# ------------------------
log() {
  echo -e "\033[1;34m$1\033[0m"
}

exists() {
  local query="$1"
  az $query &> /dev/null
}

# ------------------------
# Resource Group
# ------------------------
log "Checking for resource group '$RESOURCE_GROUP'..."
if exists "group show --name $RESOURCE_GROUP"; then
  log "Resource group exists."
else
  log "Creating resource group..."
  az group create --name $RESOURCE_GROUP --location $LOCATION
fi

# ------------------------
# ACR
# ------------------------
log "Checking for ACR '$ACR_NAME'..."
if exists "acr show --name $ACR_NAME"; then
  log "ACR exists."
else
  log "Creating ACR..."
  az acr create \
    --name $ACR_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku Basic \
    --location $LOCATION \
    --admin-enabled true
fi

# ------------------------
# AKS
# ------------------------
log "Checking for AKS cluster '$AKS_CLUSTER_NAME'..."
if exists "aks show --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER_NAME"; then
  log "AKS cluster exists."
else
  log "Creating AKS cluster (this will take a few minutes)..."
  az aks create \
    --resource-group $RESOURCE_GROUP \
    --name $AKS_CLUSTER_NAME \
    --node-count $NODE_COUNT \
    --generate-ssh-keys \
    --location $LOCATION
fi

# ------------------------
# Get AKS Credentials
# ------------------------
log "Fetching kubeconfig for kubectl access..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER_NAME --overwrite-existing

# ------------------------
# ACR Pull Secret for Kubernetes
# ------------------------
log "Checking for acr-secret in Kubernetes..."
if kubectl get secret acr-secret --namespace=default &> /dev/null; then
  log "Kubernetes image pull secret 'acr-secret' already exists."
else
  log "Creating image pull secret 'acr-secret' in Kubernetes..."

  ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
  ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
  ACR_SERVER="$ACR_NAME.azurecr.io"

  kubectl create secret docker-registry acr-secret \
    --docker-server=$ACR_SERVER \
    --docker-username=$ACR_USERNAME \
    --docker-password=$ACR_PASSWORD \
    --namespace=default
fi

log "All Azure resources and Kubernetes setup steps are complete."
