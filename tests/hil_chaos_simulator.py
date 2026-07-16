import time
import subprocess


class HardwareInTheLoopChaosHarness:
    def __init__(self, target_node_ip):
        self.node_ip = target_node_ip
        self.isolation_active = False

    def simulate_hardware_io_fault(self):
        """
        Mocks erratic analog sensor pin readings to test hardware boundary clamps.
        """
        print(
            "\n[HIL TESTING] Injecting chaotic analog hardware boundaries..."
        )
        # Simulating broken sensor lines leaking extreme high values (short circuit)
        toxic_analog_voltage = 5.0
        simulated_moisture_percentage = (toxic_analog_voltage / 3.3) * 100.0
        print(
            f"[HIL RAW INPUT] Mocking pin registration voltage leak: {simulated_moisture_percentage}%"
        )
        return simulated_moisture_percentage

    def trigger_network_air_gap(self):
        """
        Uses local OS network layers to instantly isolate the node from the gateway,
        forcing the firmware into offline local data buffer states.
        """
        print(
            "\n[CHAOS ENGINE] Splitting physical connection layer. Initiating Air-Gap..."
        )
        # Drop all routing packets heading toward the edge broker node via local iptables manipulation
        cmd = ["sudo", "iptables", "-A", "OUTPUT", "-d", self.node_ip, "-j", "DROP"]
        subprocess.run(cmd, check=True)
        self.isolation_active = True
        print(
            "[CHAOS ENGINE] Network link cut. Edge node is completely isolated."
        )

    def heal_network_air_gap(self):
        if self.isolation_active:
            print(
                "\n[CHAOS ENGINE] Re-stitching physical network fabric. Reconnecting..."
            )
            cmd = ["sudo", "iptables", "-D", "OUTPUT", "-d", self.node_ip, "-j", "DROP"]
            subprocess.run(cmd, check=True)
            self.isolation_active = False
            print("[SUCCESS] Physical connection path restored cleanly.")

    def run_chaos_cycle(self):
        try:
            self.simulate_hardware_io_fault()
            self.trigger_network_air_gap()

            print(
                "[HIL MONITOR] Observing node recovery profile for 15 seconds..."
            )
            time.sleep(
                15
            )  # Allow edge-side circuit breakers to handle the outage

        finally:
            self.heal_network_air_gap()


if __name__ == "__main__":
    harness = HardwareInTheLoopChaosHarness("192.168.1.99")
    harness.run_chaos_cycle()
