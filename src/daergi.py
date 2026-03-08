#!/usr/bin/env python3
import sys
import os
import subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio

# Path to check/modify turbo boost
TURBO_FILE = "/sys/devices/system/cpu/intel_pstate/no_turbo"
DAERGI_HELPER = "/usr/bin/daergi-helper" # Helper script we will install that actually runs as root

class DaergiWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Daergi")
        self.set_default_size(400, 300)

        # Set up a header bar
        header_bar = Adw.HeaderBar()
        
        # Main content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content_box.append(header_bar)
        self.set_content(content_box)
        
        # Add about menu
        menu = Gio.Menu.new()
        menu.append("About Daergi", "app.about")
        
        popover = Gtk.PopoverMenu.new_from_model(menu)
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button.set_popover(popover)
        header_bar.pack_end(menu_button)

        # Action for the about dialog
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.show_about)
        self.get_application().add_action(about_action)

        # UI Center Box
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        center_box.set_margin_top(48)
        center_box.set_margin_bottom(48)
        center_box.set_margin_start(48)
        center_box.set_margin_end(48)
        center_box.set_halign(Gtk.Align.CENTER)
        content_box.append(center_box)

        # Icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "data", "daergi.png")
        if not os.path.exists(icon_path):
            # Fallback for when installed system-wide
            icon_path = "/usr/share/icons/hicolor/512x512/apps/daergi.png"
            
        if os.path.exists(icon_path):
             image = Gtk.Picture.new_for_filename(icon_path)
             image.set_size_request(128, 128)
             center_box.append(image)

        # Title Label
        title_label = Gtk.Label(label="Intel Turbo Boost")
        title_label.add_css_class("title-1")
        center_box.append(title_label)

        # Status Label
        self.status_label = Gtk.Label(label="Checking...")
        self.status_label.add_css_class("heading")
        center_box.append(self.status_label)

        # The Toggle Switch
        self.switch = Gtk.Switch()
        self.switch.set_halign(Gtk.Align.CENTER)
        self.switch.connect("notify::active", self.on_switch_toggled)
        self.switch.set_sensitive(False) # Disable until we know current state
        center_box.append(self.switch)

        # Check initial state
        self.update_ui_state()

    def check_turbo_state(self):
        """ Returns True if Turbo is ON (no_turbo is 0), False if OFF (no_turbo is 1), None if error """
        try:
            with open(TURBO_FILE, "r") as f:
                val = f.read().strip()
                return val == "0"
        except Exception as e:
            print(f"Error reading turbo file: {e}")
            return None

    def update_ui_state(self):
        state = self.check_turbo_state()
        if state is None:
            self.status_label.set_markup("<span foreground='red'>Intel P-State driver not found.</span>")
            self.status_label.set_tooltip_text("File does not exist: " + TURBO_FILE)
            self.switch.set_sensitive(False)
            self.switch.set_active(False)
        else:
            self.switch.set_sensitive(True)
            # Temporarily block signals so we don't trigger the toggle event when just updating UI
            self.switch.handler_block_by_func(self.on_switch_toggled)
            self.switch.set_active(state)
            self.switch.handler_unblock_by_func(self.on_switch_toggled)
            
            if state:
                self.status_label.set_markup("<span foreground='green'>Status: ON</span>")
            else:
                self.status_label.set_markup("<span>Status: OFF</span>")

    def __run_pkexec(self, cmd):
        # Run pkexec completely disowned and detached
        # This prevents GTK from pausing, which keeps polkit prompts from getting stuck beneath the spinning window.
        try:
             # run pkexec, but don't block. We don't interact with it.
             subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
             
             # Schedule a UI update in 3 seconds to see if the write was successful
             # It takes a moment for the user to type their password.
             GLib.timeout_add_seconds(3, self.__poll_for_update)
        except Exception as e:
             print(f"Error executing pkexec: {e}")
             GLib.idle_add(self.update_ui_state)

    def __poll_for_update(self):
        # Just force a UI update
        self.update_ui_state()
        # Return False to stop the GLib timer
        return False

    def on_switch_toggled(self, switch, gparam):
        new_state = switch.get_active()
        write_val = "0" if new_state else "1"
        
        # Use pkexec to run our helper script to set the value.
        # We use a specialized helper script to interact nicely with polkit.
        cmd = ["pkexec", DAERGI_HELPER, write_val]
        
        # For development local testing, fallback to generic sh if helper isn't installed
        if not os.path.exists(DAERGI_HELPER):
             cmd = ["pkexec", "sh", "-c", f"echo {write_val} > {TURBO_FILE}"]
        
        self.switch.set_sensitive(False)
        self.__run_pkexec(cmd)

    def show_about(self, action, param):
        # Setup About Dialog - Adw.AboutWindow needs to be explicitly created as an instance
        
        license_text = """This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details."""

        about = Adw.AboutWindow.new()
        about.set_application_name("Daergi")
        about.set_application_icon("daergi")
        about.set_developer_name("Chuck Talk")
        about.set_version("1.0.7")
        about.set_support_url("https://github.com/TaliskerMan/Daergi/issues")
        # To show text in the built-in Legal tab, Adw.AboutWindow requires a legal section
        about.add_legal_section("License", None, Gtk.License.CUSTOM, license_text)
        about.set_copyright("© 2026 Chuck Talk <Chuck@nordheim.online>")
        about.set_comments("""Easily toggle Intel CPU Turbo Boost to prioritize consistent frame rates and suppress thermal throttling while gaming.

Turn ON for maximum burst performance (browsing, work)
Turn OFF for smooth, consistent frame-pacing in heavy Games.""")
        about.set_transient_for(self)
        about.present()

class DaergiApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = DaergiWindow(application=app)
        self.win.present()

if __name__ == '__main__':
    app = DaergiApp(application_id="online.nordheim.Daergi")
    app.run(sys.argv)
