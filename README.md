
```
# Multi-Switch Flow Table Analyzer

## Problem Statement
Analyze flow tables in multiple SDN switches and display rule usage dynamically using Mininet and POX OpenFlow controller. The analyzer retrieves flow entries, displays rule details, identifies active vs unused rules, and updates dynamically every 5 seconds.

## Tools & Technologies
- Mininet — Network emulator
- POX — OpenFlow controller
- Python 3 — Analyzer script
- OVS (Open vSwitch) — Virtual switch
- ovs-ofctl — Flow table querying

## Topology
3 switches (s1, s2, s3) connected in a linear chain, each with 2 hosts:
- s1 → h1, h2
- s2 → h3, h4
- s3 → h5, h6

## How to Run

Open 3 terminals:

**Terminal 1 — Start POX Controller**
```
cd ~/pox
python3 pox.py openflow.of_01 --port=6633 flow_controller
```

**Terminal 2 — Start Mininet Topology**
```
cd ~/flow_project
sudo python3 multi_switch_topo.py
```

**Terminal 3 — Start Flow Analyzer**
```
cd ~/flow_project
sudo python3 flow_analyzer.py
```

## Test Scenarios

**Scenario 1 — pingall (all hosts)**
Run inside Mininet CLI: pingall
Result: 0% dropped (30/30 received), 72 Active rules across all switches

**Scenario 2 — h1 ping h2 (single pair)**
Run inside Mininet CLI: h1 ping h2 -c 1
Result: Only s1 shows 6 active rules, s2 and s3 rules expire (unused)

## Screenshots

### Terminal 1 — POX Controller
![Terminal 1](screenshots/Terminal_1.png)

### Terminal 2 — Scenario 1: pingall
![Terminal 2](screenshots/Terminal_2.png)

### Terminal 3 — Scenario 1: 72 active rules
![Terminal 3](screenshots/terminal_3.png)

### Terminal 2 — Scenario 2: h1 ping h2
![Terminal 2 Scenario 2](screenshots/Terminal_2_2_.png)

### Terminal 3 — Scenario 2: s1 active, s2 and s3 expired
![Terminal 3 Scenario 2](screenshots/Terminal3_2_.png)

## References
- Mininet: http://mininet.org
- POX Controller: https://github.com/noxrepo/pox
- OpenFlow: https://opennetworking.org/sdn-resources/openflow/
```
