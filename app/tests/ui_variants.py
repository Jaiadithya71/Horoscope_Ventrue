"""Synthetic charts only. Regression fixture covering all 12 rising signs."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from api.calculate import calculate
out=[]
for h in range(24):
    birth=dict(date='1990-06-15',time=f'{h:02}:00',timezone='Asia/Kolkata',place='Synthetic test',latitude=13.,longitude=80.)
    out.append(dict(birth=birth,report=calculate(dict(birth=birth,tamil_view=True,node_mode='mean' if h%2 else 'true'))))
print(json.dumps(out))
