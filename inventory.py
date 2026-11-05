"""Write file inventory, tested versions and provenance hashes after exports."""
from common import *
import hashlib,platform
import PIL,cv2
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data').glob('*')) if p.is_file() and p.name!='SHA256.json'}
(ROOT/'data/SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
environment={'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__,'Pillow':PIL.__version__,'opencv-python':cv2.__version__,'exportBackend':matplotlib.get_backend(),'videoCodec':'mp4v / MPEG-4 Part 2','interactiveBackendRequired':True}
(ROOT/'outputs/environment.json').write_text(json.dumps(environment,indent=2)+'\n')
manifest=[]
for p in sorted((ROOT/'outputs').rglob('*')):
 if p.suffix not in ['.png','.pdf','.gif','.mp4']:continue
 name=p.stem
 limitation='Computed routes on fixed instance; no neural inference.'
 if name.startswith('01'):limitation='Only a nearby-edge subset is drawn; mathematical graph is complete.'
 if name=='02-cw-merges':limitation='Discrete merge history, not continuous driving; use 02-cw-routes for motion.'
 if name.startswith('03'):limitation='Saved classical candidates; Python centroid selection and exact pool DP. No global certificate. Representative candidates only.'
 if name.startswith('04'):limitation='Local single-route mask, not an AM execution. The path is fixed.'
 if name.startswith('05'):limitation='Conceptual POMO starts/symmetries; no neural rollouts. Starts do not form one feasible fleet.'
 if name.startswith('06'):limitation='Saved station insertion; Python travel/fuel/time states. No time mask during construction or CO2 model.'
 if name.startswith('07'):limitation='Saved MILP results. Proven optimal only for exactly seven active routes. At-most-seven incumbent not proven optimal.'
 e={'path':str(p.relative_to(ROOT)),'format':p.suffix[1:].upper(),'bytes':p.stat().st_size,'limitation':limitation}
 verification=p.with_suffix('.verification.json')
 if verification.exists() and p.suffix in ['.gif','.mp4']:e['mediaVerification']=json.loads(verification.read_text())
 manifest.append(e)
(ROOT/'outputs/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Inventory:',len(manifest),'figure/media files')
