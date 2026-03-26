#!/bin/bash
# Daergi 1.0.8 GitHub Release Publisher

echo "Publishing Daergi 1.0.8 release to GitHub..."

gh release create v1.0.8 \
  --title "Daergi 1.0.8 - Critical Security Update" \
  --notes "A critical Local Privilege Escalation (LPE) vulnerability affecting the Polkit authentication flow mapped to the daergi-helper script has been remediated. All users are urged to update immediately.

Additional Hardening:
- Stripped arbitrary GUI evaluation permissions from the headless background processes.
- Removed a hardcoded dynamic shell evaluation fallback loop." \
  daergi_1.0.8_all.deb \
  daergi_1.0.8_all.deb.sha512 \
  daergi_1.0.8_all.deb.asc

echo "Release successfully published!"
