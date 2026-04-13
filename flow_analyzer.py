import subprocess
import time
import os
from datetime import datetime

SWITCHES = ['s1', 's2', 's3']
POLL_INTERVAL = 5

def get_flows(switch):
    try:
        result = subprocess.run(
            ['sudo', 'ovs-ofctl', 'dump-flows', switch],
            capture_output=True, text=True)
        return result.stdout.strip().split('\n')[1:]
    except Exception as e:
        return [f"Error: {e}"]

def classify(flow):
    try:
        n_packets = [x for x in flow.split(',') if 'n_packets' in x]
        if n_packets:
            count = int(n_packets[0].split('=')[1].strip())
            return "ACTIVE" if count > 0 else "UNUSED"
    except:
        pass
    return "UNUSED"

def display(switch, flows):
    print(f"\n{'='*60}")
    print(f"  Switch: {switch}  |  Rules: {len(flows)}")
    print(f"  Polled at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    active = 0
    unused = 0
    for flow in flows:
        if not flow or flow.startswith('Error'):
            print(f"  {flow}")
            continue
        status = classify(flow)
        if status == "ACTIVE":
            active += 1
            tag = "[ACT]"
        else:
            unused += 1
            tag = "[---]"
        print(f"  {tag}  {flow[:80]}")
    print(f"\n  Summary -> Active: {active}  |  Unused: {unused}")

def analyze():
    print("\n[Flow Table Analyzer] Starting... (Ctrl+C to stop)")
    while True:
        os.system('clear')
        print(f"Multi-Switch Flow Table Analyzer [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        for sw in SWITCHES:
            flows = get_flows(sw)
            display(sw, flows)
        print(f"\n  Refreshing in {POLL_INTERVAL}s...")
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    analyze()
