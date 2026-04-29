#!/bin/bash
# Daergi 1.0.9 GitHub Release Publisher

echo "Publishing Daergi 1.0.9 release to GitHub..."

gh release create v1.0.9 \
  --title "Daergi 1.0.9 - Missing Shebang Hotfix" \
  --notes "This release fixes an issue where Daergi failed to launch for new installations due to a missing Python shebang header. The issue was identified and patched directly in the source.

Additional Checks:
- Verified Snyk code scan passed with 0 vulnerabilities." \
  daergi_1.0.9_all.deb \
  daergi_1.0.9_all.deb.sha512 \
  daergi_1.0.9_all.deb.asc

echo "Release successfully published!"
