

```
# Multi-Switch Flow Table Analyzer

## 1. Student Information.

| Name | SRN |
|------|-----|
| Poojitha T | PES1UG24AM192 |

---

## 2. Problem Statement
Analyze flow tables in multiple SDN switches and display rule usage dynamically using Mininet and POX OpenFlow controller. The analyzer retrieves flow entries, displays rule details, identifies active vs unused rules, and updates dynamically every 5 seconds.

---

## 3. Tools & Technologies
- Mininet — Network emulator
- POX — OpenFlow controller
- Python 3 — Analyzer script
- OVS (Open vSwitch) — Virtual switch
- ovs-ofctl — Flow table querying

---

## 4. Topology
3 switches (s1, s2, s3) connected in a linear chain, each with 2 hosts:
- s1 → h1, h2
- s2 → h3, h4
- s3 → h5, h6
- Links: s1-s2, s2-s3

---

## 5. Setup & Installation

### Prerequisites
```bash
sudo apt install mininet python3-pip git -y
pip3 install setuptools==58.0.0 --break-system-packages
pip3 install ryu --break-system-packages
```

### Clone POX Controller
```bash
cd ~
git clone https://github.com/noxrepo/pox.git
cp flow_controller.py ~/pox/ext/flow_controller.py
```

---

## 6. How to Run

Open 3 terminals:

### Terminal 1 — Start POX Controller
```bash
cd ~/pox
python3 pox.py openflow.of_01 --port=6633 flow_controller
```
Wait until you see:
```
INFO:flow_controller:Switch 00-00-00-00-00-01 connected.
INFO:flow_controller:Switch 00-00-00-00-00-02 connected.
INFO:flow_controller:Switch 00-00-00-00-00-03 connected.
```

### Terminal 2 — Start Mininet Topology
```bash
cd ~/flow_project
sudo python3 multi_switch_topo.py
```

### Terminal 3 — Start Flow Analyzer
```bash
cd ~/flow_project
sudo python3 flow_analyzer.py
```

---

## 7. Test Scenarios

### Scenario 1 — All hosts communicating (pingall)
Run inside Mininet CLI:
```bash
pingall
```
- Result: 0% dropped (30/30 received)
- Flow Analyzer: 72 Active rules, 0 Unused across all 3 switches
- All rules marked [ACT] with packet counts > 0

### Scenario 2 — Single host pair (h1 ping h2)
Run inside Mininet CLI:
```bash
h1 ping h2 -c 1
```
- Result: 0% packet loss
- Flow Analyzer: s1 shows 6 Active rules for h1↔h2 only
- s2 and s3 show 0 rules — all rules expired due to idle_timeout=30
- Demonstrates active vs unused rule identification

---

## 8. Demo Screenshots

### Screenshot 1 — POX Controller (all 3 switches connected)
All 3 switches successfully connected to the POX controller via OpenFlow.
![Terminal 1](screenshots/Terminal_1.png)

### Screenshot 2 — Scenario 1: pingall result
All 6 hosts communicating across all 3 switches with 0% packet loss.
![Terminal 2 Scenario 1](screenshots/Terminal_2.png)

### Screenshot 3 — Scenario 1: Flow Analyzer after pingall
72 active flow rules detected across all switches, all marked [ACT].
![Terminal 3 Scenario 1](screenshots/terminal_3.png)

### Screenshot 4 — Scenario 2: h1 ping h2
Single host pair communication with 0% packet loss.
![Terminal 2 Scenario 2](screenshots/Terminal_2_2_.png)

### Screenshot 5 — Scenario 2: Flow Analyzer after h1 ping h2
Only s1 shows 6 active rules for h1↔h2. s2 and s3 rules expired (unused).
![Terminal 3 Scenario 2](screenshots/Terminal3_2_.png)

---

## 9. Engineering Analysis

### Flow Rule Lifecycle
When a packet arrives at a switch with no matching flow rule, it is sent to the POX controller as a packet_in event. The controller's learning switch logic inspects the source MAC address, records which port it came from, and installs a flow rule so future packets to that destination are forwarded directly without involving the controller. Each rule has an idle_timeout of 30 seconds — if no matching traffic is seen for 30 seconds, the rule is automatically removed by the switch.

### Active vs Unused Rule Detection
The flow analyzer uses ovs-ofctl dump-flows to retrieve all flow entries from each switch every 5 seconds. Each entry contains an n_packets counter showing how many packets have matched that rule. Rules with n_packets > 0 are classified as [ACT] (active), while rules with n_packets = 0 are classified as [---] (unused). After idle_timeout expires, rules disappear entirely from the flow table.

### Multi-Switch Traffic Flow
When h1 pings h6, the packet must traverse s1 → s2 → s3. The POX controller installs flow rules on all three switches along the path. This is visible in Scenario 1 where all 3 switches show active rules after pingall, and in Scenario 2 where only s1 has rules after h1 pings h2 (which are on the same switch).

### Dynamic Updates
The analyzer runs in an infinite loop, polling all switches every 5 seconds and clearing the screen between updates. This allows real-time observation of rule installation and expiry, demonstrating the dynamic nature of SDN flow table management.

---

## 10. Design Decisions and Tradeoffs

### POX over Ryu
We chose POX as the OpenFlow controller instead of Ryu due to compatibility issues between Ryu and Python 3.11. POX supports OpenFlow 1.0 and works reliably with the installed Python version. The tradeoff is that POX does not provide a REST API out of the box, so the flow analyzer uses ovs-ofctl instead of HTTP requests to retrieve flow tables.

### ovs-ofctl for Flow Retrieval
Instead of using a controller REST API, the analyzer directly queries Open vSwitch using ovs-ofctl dump-flows. This is more reliable since it does not depend on any controller-side API. The tradeoff is that it requires sudo privileges to run.

### idle_timeout=30
Flow rules are installed with an idle_timeout of 30 seconds. This means unused rules expire automatically, keeping flow tables clean and demonstrating the active vs unused distinction clearly. A longer timeout would keep rules alive longer but make the unused state harder to observe.

### Linear Topology
A linear chain (s1-s2-s3) was chosen because it forces traffic between h1 and h6 to traverse all three switches, demonstrating multi-switch flow rule installation clearly. A star topology would not show inter-switch flow propagation as effectively.

---

## 11. References
- Mininet: http://mininet.org
- POX Controller: https://github.com/noxrepo/pox
- OpenFlow Specification: https://opennetworking.org/sdn-resources/openflow/
- ovs-ofctl Manual: https://man7.org/linux/man-pages/man8/ovs-ofctl.8.html
```

