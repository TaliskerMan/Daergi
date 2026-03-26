<div align="center">
  <img src="data/daergi.png" alt="Daergi Icon" width="128" />
  <h1>Daergi</h1>
  <p>A simple, lightweight GTK4 application to manage Intel Turbo Boost on Linux.</p>
</div>

## About
Daergi (Welsh for Terrier) allows gamers and power users to easily toggle their Intel CPU's Turbo Boost feature on and off. Disabling Turbo Boost can help provide consistent frame rates without jarring stutters during intensive operations like gaming, at the cost of peak burst performance.

## Installation

1. Download the latest `daergi_X.X_all.deb` and the detached signature `.sig` from the Releases page.
2. Verify the SHA512 hash and GPG detached signature.
3. Install using `apt`:
   ```bash
   sudo apt install ./daergi_X.X_all.deb
   ```

## Usage
1. Launch Daergi from your GNOME Dock or AppGrid.
2. The UI will clearly show your current system Turbo Boost status.
3. Click the toggle switch to Turn Off or Turn On Turbo Boost. 
4. You will be prompted for your password via standard Polkit authentication to apply the changes as an administrator smoothly.

## Troubleshooting
- **App doesn't toggle state:** Double-check that your CPU driver is `intel_pstate`. You can verify this by checking if the file `/sys/devices/system/cpu/intel_pstate/no_turbo` exists on your system.
- **Authentication fails:** Ensure your user account is added to the `sudo` or `wheel` group on your Linux distribution, as `pkexec` requires standard administrative rights.

## License
This project is licensed under the GNU GPL v3.  
Copyright (C) 2026 Chuck Talk <Chuck@nordheim.online>
