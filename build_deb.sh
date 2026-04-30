#!/bin/bash
# Description: Build Daergi DEB package securely with correct root ownership

set -e

echo "Copying latest source files to debian directory..."
cp src/daergi.py debian/daergi/usr/bin/daergi
cp src/daergi-helper debian/daergi/usr/bin/daergi-helper
cp src/daergi.desktop debian/daergi/usr/share/applications/daergi.desktop
cp src/online.nordheim.daergi.policy debian/daergi/usr/share/polkit-1/actions/online.nordheim.daergi.policy
cp data/daergi.png debian/daergi/usr/share/daergi/daergi.png
cp data/daergi.png debian/daergi/usr/share/icons/hicolor/512x512/apps/daergi.png
cp data/daergi.png debian/daergi/usr/share/icons/hicolor/128x128/apps/daergi.png

# Ensure permissions are correct
chmod +x debian/daergi/usr/bin/daergi
chmod +x debian/daergi/usr/bin/daergi-helper

# Get version from control file
VERSION=$(grep Version debian/daergi/DEBIAN/control | cut -d' ' -f2)

echo "Building secure DEB package version $VERSION..."
# Use --root-owner-group to prevent local privilege escalation vulnerability
dpkg-deb --root-owner-group --build debian/daergi "daergi_${VERSION}_all.deb"

echo "Generating SHA512 hash and GPG detach signature..."
sha512sum "daergi_${VERSION}_all.deb" > "daergi_${VERSION}_all.deb.sha512"
gpg --local-user "chuck@nordheim.online" --detach-sign --armor "daergi_${VERSION}_all.deb"

echo "Package daergi_${VERSION}_all.deb has been built successfully."
