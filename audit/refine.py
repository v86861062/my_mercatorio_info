"""Refine the transferred audit fixture without relaxing the page CSP."""
from pathlib import Path
import hashlib
p = Path('.audit-runtime/test.py')
t = p.read_text()
old = "page.wait_for_function('!!window.ATLAS')"
assert t.count(old) == 2
# Poll a DOM condition, not a string evaluated inside the page's CSP.
t = t.replace(old, "page.locator('#loading-status').wait_for(state='hidden');assert page.evaluate('() => Boolean(window.ATLAS)')")
marker = "examples=['bake bread 1'"
assert marker in t
checks = '''upgrade_checks=0
for recipe in R.values():
 facility=d['buildings'].get(recipe['building']) or d['transports'].get(recipe['building'])
 if facility:
  upgrades={x['type'] for x in facility['raw_definition'].get('upgrades',[])}
  for upgrade in recipe['raw_definition'].get('upgrades',[]):
   assert upgrade in upgrades,(recipe['id'],upgrade)
   upgrade_checks+=1
assert upgrade_checks==343
'''
t=t.replace(marker, checks+marker)
t=t.replace("'raw_recipes_exact':694,", "'raw_recipes_exact':694,'upgrade_references_exact':upgrade_checks,")
p.write_text(t)
# Preserve English source units where a Chinese equivalent would be ambiguous.
if not Path('audit/ready').read_text().startswith('live:'):
 p=Path('assets/industry-tree.js');t=p.read_text()
 for item in ["stone:'石',", "quire:'刀',", "quarter:'夸特',"]:
  assert t.count(item)==1
  t=t.replace(item,'')
 p.write_text(t)
print('CSP-safe test SHA256:',hashlib.sha256(Path('.audit-runtime/test.py').read_bytes()).hexdigest())
print('Industry JS SHA256:',hashlib.sha256(Path('assets/industry-tree.js').read_bytes()).hexdigest())
