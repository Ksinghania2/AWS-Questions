#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Install PowerShell
#
# Purpose:
#   Installs PowerShell for working with S3 from Windows/Linux shells.
#
# Usage:
#   ./bin/powershell_cli_install.sh
################################################################################

echo "Installing PowerShell..."

# If PowerShell is already installed, stop here.
if command -v pwsh >/dev/null 2>&1; then
  echo "PowerShell is already installed: $(pwsh --version)"
  exit 0
fi

# Read the OS version so we can install the correct package source.
if [[ -f /etc/os-release ]]; then
  . /etc/os-release
fi

case "${ID:-ubuntu}" in
  ubuntu)
    # Default to Ubuntu 22.04 if the version is not known.
    VERSION_ID="${VERSION_ID:-22.04}"
    case "$VERSION_ID" in
      22.04|24.04)
        # Download the Microsoft package source and install PowerShell.
        wget -q "https://packages.microsoft.com/config/ubuntu/$VERSION_ID/packages-microsoft-prod.deb" -O /tmp/packages-microsoft-prod.deb
        sudo dpkg -i /tmp/packages-microsoft-prod.deb
        sudo apt-get update
        sudo apt-get install -y powershell
        ;;
      *)
        echo "Unsupported Ubuntu version: $VERSION_ID"
        exit 1
        ;;
    esac
    ;;
  debian)
    echo "Please install PowerShell manually for Debian."
    exit 1
    ;;
  *)
    echo "Please install PowerShell manually for this OS."
    exit 1
    ;;
esac

echo "PowerShell installation completed."
echo "Verify with: pwsh --version"
