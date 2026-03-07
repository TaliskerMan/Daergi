# Daergi Implementation Plan

## Overview
**Daergi** (Welsh for Terrier) is a simple, lightweight GTK4 application to manage Intel Turbo Boost on Linux, allowing users to toggle Turbo Boost on/off for consistent frame rates in games.

## Tech Stack
- Python 3
- GTK4 / libadwaita (via PyGObject)
- `pkexec` (PolicyKit for root rights to write to `/sys/devices/...`)
- Debian Packaging (`dpkg-deb`)
- GPG (for detached signatures and SHA512 hashsums)
- Git / GitHub (Public Repo)

## Core Features
1. **Toggle UI:** Simple window with status indicator and main toggle switch.
2. **About Page:** Contains GNU GPL v3 license details and copyright ("Chuck Talk", email "Chuck@nordheim.online").
3. **Authentication:** Integrates with Polkit to smoothly prompt user for password when changing the system state.
4. **App Integration:** Provides a standard `.desktop` file for the GNOME Dock and AppGrid, integrating the custom Daergi icon.

## Repo Structure
- `data/`: Contains the icon image and any desktop/policy files.
- `docs/`: Plan files (this document), future feature enhancements, design thoughts.
- `src/`: Python source code containing the actual GTK logic.
- `debian/`: Structure to generate the `.deb` release package.

## Packaging & Verification
- Output will be a clean `daergi_X.X-X_all.deb` package.
- Release workflow will use `sha512sum` for integrity.
- Release assets will be signed using GPG (`gpg --detach-sign --armor`) for verified software distribution.
