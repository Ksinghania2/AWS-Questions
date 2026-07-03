#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Install AWS CLI v2
#
# Purpose:
#   Installs the AWS CLI on a Linux environment for S3 and AWS automation.
#
# Usage:
#   ./bin/aws_cli_install.sh
################################################################################

echo "Installing AWS CLI v2..."

# If AWS CLI is already present, skip the install.
if command -v aws >/dev/null 2>&1; then
  echo "AWS CLI is already installed: $(aws --version)"
  exit 0
fi

# We need sudo because the install writes to system folders.
if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required to install AWS CLI."
  exit 1
fi

# Read OS details so we can choose the right package commands.
if [[ -f /etc/os-release ]]; then
  . /etc/os-release
fi

case "${ID:-ubuntu}" in
  ubuntu|debian)
    # Update package lists and install the tools needed for the AWS CLI archive.
    sudo apt-get update
    sudo apt-get install -y unzip curl
    # Download and extract the AWS CLI installer.
    curl -sSLo /tmp/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
    unzip -q /tmp/awscliv2.zip -d /tmp/
    # Run the official AWS CLI installer.
    sudo /tmp/aws/install
    ;;
  centos|rhel|fedora)
    sudo dnf install -y unzip curl
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip
    unzip -q /tmp/awscliv2.zip -d /tmp/
    sudo /tmp/aws/install
    ;;
  *)
    echo "Unsupported OS. Please install AWS CLI manually."
    exit 1
    ;;
esac

echo "AWS CLI installation completed."
echo "Verify with: aws --version"
