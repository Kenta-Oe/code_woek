#!/bin/bash

set -e

REF_DIR="/usr/share/jenkins/ref/plugins"
JENKINS_UC_DOWNLOAD="https://updates.jenkins.io"

mkdir -p $REF_DIR

installPlugin() {
  local plugin="$1"
  local version="${2:-latest}"
  echo "Attempting to install plugin: ${plugin}, version: ${version}"
  if [ "$version" == "latest" ]; then
    version=$(curl -sSL "${JENKINS_UC_DOWNLOAD}/latest/${plugin}.hpi" -o /dev/null -w '%{url_effective}' | awk -F'/' '{print $(NF-1)}') || { echo "Failed to retrieve version for ${plugin}"; exit 1; }
  fi
  echo "Installing ${plugin} version ${version}"
  curl -sSL -f "${JENKINS_UC_DOWNLOAD}/download/plugins/${plugin}/${version}/${plugin}.hpi" -o "${REF_DIR}/${plugin}.hpi" || { echo "Failed to download ${plugin}"; exit 1; }
}

while IFS=: read -r plugin version; do
  installPlugin "$plugin" "$version"
done < /usr/share/jenkins/ref/plugins.txt
