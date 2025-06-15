#!/bin/bash

# ------------------------
# Configurable Variables
# ------------------------
DEPLOYMENT_FILE="deployment.yaml"
APP_NAME_OLD="telemetry-worker"
APP_NAME_NEW="azurekubelogger"
ACR_NAME="cogstakacr"
ACR_IMAGE_TAG="latest"
IMAGE_PATH="$ACR_NAME.azurecr.io/$APP_NAME_NEW:$ACR_IMAGE_TAG"
IMAGE_PULL_SECRET_NAME="acr-secret"

# ------------------------
# Helper Functions
# ------------------------
log() {
  echo -e "\033[1;34m$1\033[0m"
}

file_check() {
  if [ ! -f "$DEPLOYMENT_FILE" ]; then
    echo "$DEPLOYMENT_FILE not found."
    exit 1
  fi
}

replace_app_names() {
  log "Replacing app references from '$APP_NAME_OLD' → '$APP_NAME_NEW'..."
  sed -i.bak \
    -e "s/name: $APP_NAME_OLD/name: $APP_NAME_NEW/g" \
    -e "s/app: $APP_NAME_OLD/app: $APP_NAME_NEW/g" \
    "$DEPLOYMENT_FILE"
}

update_image() {
  log "Updating container image to '$IMAGE_PATH'..."
  sed -i.bak "s|image: .*|image: $IMAGE_PATH|g" "$DEPLOYMENT_FILE"
}

inject_pull_secret() {
  log "Checking for imagePullSecrets..."
  if grep -q "imagePullSecrets" "$DEPLOYMENT_FILE"; then
    log "imagePullSecrets already present."
  else
    log "Adding imagePullSecrets..."
    # insert imagePullSecrets below containers block
    awk -v indent="      " -v secret="$IMAGE_PULL_SECRET_NAME" '
    /^ *containers:/ { print; found=1; next }
    found && /^ *restartPolicy:/ {
      print indent "imagePullSecrets:"
      print indent "  - name: " secret
      found=0
    }
    { print }
    ' "$DEPLOYMENT_FILE" > temp.yaml && mv temp.yaml "$DEPLOYMENT_FILE"
  fi
}

clean_backup() {
  rm -f "$DEPLOYMENT_FILE.bak"
}

# ------------------------
# Script Execution
# ------------------------
file_check
replace_app_names
update_image
inject_pull_secret
clean_backup

log "deployment.yaml is ready for GitHub Actions + AKS deployment."