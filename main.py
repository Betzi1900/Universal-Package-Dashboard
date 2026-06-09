import tkinter as tk
from tkinter import ttk, messagebox
import traceback

# Hier laden wir den neuen Router für die Open-Source-Architektur
from tracker import UniversalTracker
from database import Database


class LinuxDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Dashboard - Paket Tracker")
        self.root.geometry("800x400")

        # Module initialisieren
        self.db = Database()
        self.tracker = UniversalTracker()

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Oberer Bereich: Eingabe
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill=tk.X, padx=10)

        tk.Label(input_frame, text="Sendungsnummer:").pack(side=tk.LEFT, padx=5)
        self.entry_tracking = tk.Entry(input_frame, width=30)
        self.entry_tracking.pack(side=tk.LEFT, padx=5)

        # Aktuell noch fest auf DHL, später kommt hier ein Dropdown-Menü hin
        btn_add = tk.Button(input_frame, text="Paket hinzufügen", command=self.add_package)
        btn_add.pack(side=tk.LEFT, padx=5)

        btn_refresh = tk.Button(input_frame, text="Status aktualisieren", command=self.refresh_all_packages)
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Unterer Bereich: Die Tabelle
        columns = ("tracking_number", "carrier", "status", "sender")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        self.tree.heading("tracking_number", text="Sendungsnummer")
        self.tree.heading("carrier", text="Dienstleister")
        self.tree.heading("status", text="Aktueller Status")
        self.tree.heading("sender", text="Absender")

        self.tree.column("tracking_number", width=150)
        self.tree.column("carrier", width=100)
        self.tree.column("status", width=350)
        self.tree.column("sender", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_data(self):
        # Tabelle leeren
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Daten aus SQL laden und anzeigen
        packages = self.db.get_all_packages()
        for pkg in packages:
            self.tree.insert("", tk.END, values=pkg)

    def add_package(self):
        number = self.entry_tracking.get().strip()
        if not number:
            messagebox.showwarning("Fehler", "Bitte eine Sendungsnummer eingeben!")
            return

        # In DB speichern (Carrier ist standardmäßig DHL)
        if self.db.add_package(number, "DHL"):
            self.entry_tracking.delete(0, tk.END)
            self.load_data()
            # Direkt ein initiales Update anstoßen
            self.refresh_all_packages()
        else:
            messagebox.showinfo("Info", "Dieses Paket ist bereits im Dashboard.")

    def refresh_all_packages(self):
        packages = self.db.get_all_packages()

        for pkg in packages:
            tracking_number = pkg[0]
            carrier = pkg[1]

            print(f"Aktualisiere Paket: {tracking_number} ({carrier})")

            # Die Anfrage geht jetzt an den neuen UniversalTracker
            result = self.tracker.track_package(tracking_number, carrier)

            if "shipment" in result:
                new_status = result["shipment"]["status"]
                new_sender = result["shipment"]["sender"]
                self.db.update_package_status(tracking_number, new_status, new_sender)
            elif "error" in result:
                print(f"Fehler bei {tracking_number}: {result['error']}")

        # GUI nach dem Update neu zeichnen
        self.load_data()


# ====================================================================
# START-BLOCK (Komplett linksbündig!)
# ====================================================================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LinuxDashboard(root)
        root.mainloop()
    except Exception as e:
        print("\n" + "=" * 50)
        print("KRITISCHER FEHLER BEIM STARTEN DES DASHBOARDS:")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)
        input("\nDrücke ENTER zum Beenden...")