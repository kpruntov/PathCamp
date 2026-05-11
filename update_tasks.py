import json
import glob
import os

files = glob.glob('.spec/data/06_execution/task_*.json')
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
    
    if 'UI Component' in data.get('title', '') or 'UI ' in data.get('title', ''):
        if 'trace_to' not in data:
            data['trace_to'] = {}
        if 'constraints' not in data['trace_to']:
            data['trace_to']['constraints'] = []
        if "CON-001" not in data['trace_to']['constraints']:
            data['trace_to']['constraints'].append("CON-001")
        if "CON-002" not in data['trace_to']['constraints']:
            data['trace_to']['constraints'].append("CON-002")
        
        with open(file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {file}")
