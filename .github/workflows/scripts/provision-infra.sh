#!/bin/bash

set -euo pipefail

RESOURCE_GROUP="cogstak-realtime-services"
LOCATION="westus2"
ACR_NAME="cogstakacr"
AKS_NAME="cogstak-aks-cluster"

log() {
  echo -e "\033[1;32m[INFO]\033[0m $1"
}

error() {
  echo -e "\033[1;31m[ERROR]\033[0m $1" >&2
}

log "Creating resource group (if not exists)..."
az group show --name $RESOURCE_GROUP || az group create --name $RESOURCE_GROUP --location $LOCATION

log "Registering required Azure providers..."
az provider register --namespace Microsoft.ContainerRegistry
az provider register --namespace Microsoft.ContainerService

log "Creating Azure Container Registry (ACR)..."
az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP || az acr create --name $ACR_NAME --sku Basic --resource-group $RESOURCE_GROUP --location $LOCATION

log "Creating Azure Kubernetes Service (AKS) cluster..."
az aks show --name $AKS_NAME --resource-group $RESOURCE_GROUP || az aks create --name $AKS_NAME --resource-group $RESOURCE_GROUP --node-count 1 --generate-ssh-keys --attach-acr $ACR_NAME
