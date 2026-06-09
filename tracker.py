# tracker.py
from dhl_api import DHLTracker


# from hermes_api import HermesTracker  <-- Das bereiten wir für später vor!

class UniversalTracker:
    def __init__(self):
        self.dhl = DHLTracker()
        # self.hermes = HermesTracker()

    def track_package(self, tracking_number, carrier):

        carrier = str(carrier).strip().upper()

        if carrier == "DHL":
            return self.dhl.track(tracking_number)

        elif carrier == "HERMES":
            return {"error": "Hermes-Tracking ist noch in Entwicklung."}

        elif carrier == "DPD":
            return {"error": "DPD-Tracking ist noch in Entwicklung."}

        else:
            return {"error": f"Dienstleister '{carrier}' wird nicht unterstützt."}