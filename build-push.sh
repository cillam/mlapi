#!/bin/bash

# Exit on any error
set -e

# Set variables
IMAGE_PREFIX=<NAMESPACE>
IMAGE_NAME=<IMAGE_NAME>
ACR_NAME=<ACR_NAME>
ACR_DOMAIN="${ACR_NAME}.azurecr.io"
IMAGE_FQDN="${ACR_DOMAIN}/${IMAGE_PREFIX}/${IMAGE_NAME}"
KUSTOMIZATION_PATH=".k8s/overlays/prod/kustomization.yaml" 

# Get the short commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
TAG="${COMMIT_HASH}"

echo "Current image tag will be ${TAG}"

# Login to Azure Container Registry
echo "Logging into ACR..."
az acr login --name ${ACR_NAME}

# Build docker image
echo "Building Docker image..."
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .

# Create alias of image
echo "Aliasing Docker image as ${IMAGE_FQDN}:${TAG}..."
docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_FQDN}:${TAG}

# Push image to ACR
echo "Pushing image to ACR..."
docker push ${IMAGE_FQDN}:${TAG}

# Update the kustomization.yaml with the new tag
echo "Updating kustomization.yaml with new tag..."
export TAG
if [ -f "$KUSTOMIZATION_PATH" ]; then
    yq -i '.images[].newTag = env(TAG)' "$KUSTOMIZATION_PATH"
    echo "Successfully updated image tag in kustomization.yaml to: ${TAG}"
else
    echo "Warning: Kustomization file not found at $KUSTOMIZATION_PATH"
    exit 1 
fi

echo "Successfully completed:"
echo "  - Built and pushed: ${IMAGE_FQDN}:${TAG}"
echo "  - Updated kustomization.yaml with tag: ${TAG}"