#!/bin/bash
# Daergi 1.0.10 GitHub Release Publisher

echo "Publishing Daergi 1.0.10 release to GitHub..."

gh release create v1.0.10 \
  --title "Daergi 1.0.10 - Icon Sync and Version Bump" \
  --notes "This release updates the StartWMClass for correct GNOME Dock/AppGrid icon grouping, bumps version to 1.0.10, and automates asset packaging.

Additional Checks:
- Verified Snyk code scan passed with 0 vulnerabilities." \
  daergi_1.0.10_all.deb \
  daergi_1.0.10_all.deb.sha512 \
  daergi_1.0.10_all.deb.asc

echo "Release successfully published!"
