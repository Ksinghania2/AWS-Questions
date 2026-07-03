#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Install Terraform
#
# Purpose:
#   Installs Terraform for provisioning S3 resources with infrastructure as code.
#
# Usage:
#   ./bin/terraform_cli_install.sh
################################################################################

echo "Installing Terraform..."

# If Terraform is already available, skip the install.
if command -v terraform >/dev/null 2>&1; then
  echo "Terraform is already installed: $(terraform version | head -n 1)"
  exit 0
fi

# Set the Terraform version from the environment if needed.
TERRAFORM_VERSION="${TERRAFORM_VERSION:-1.9.8}"
ARCH="amd64"
DOWNLOAD_URL="https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_${ARCH}.zip"

# Download and extract the Terraform binary.
curl -sSLo /tmp/terraform.zip "$DOWNLOAD_URL"
unzip -o -q /tmp/terraform.zip -d /tmp/terraform-bin
# Install Terraform into a system path so it is available in the shell.
sudo install -m 0755 /tmp/terraform-bin/terraform /usr/local/bin/terraform

rm -rf /tmp/terraform.zip /tmp/terraform-bin

echo "Terraform installation completed."
echo "Verify with: terraform version"
