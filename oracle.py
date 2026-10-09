#!/usr/bin/env python3
# Oracle for silkscreenmath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

MARGIN = 8
FRAMES = [[25,35],[30,40],[40,50],[50,70]]
COVER = 9
WASTE = 1.2

def r2(x): return math.floor(x * 100 + 0.5) / 100

def frameFit(imgW, imgH):
    needW = imgW + 2 * MARGIN
    needH = imgH + 2 * MARGIN
    for fw, fh in FRAMES:
        if needW <= fw and needH <= fh:
            sw, sh = r2(fw - needW), r2(fh - needH)
            return {'frame': f'{fw} x {fh}', 'orientation': 'portrait', 'spare_w': sw, 'spare_h': sh,
                    'verdict': 'snug fit' if min(sw, sh) < 6 else 'room to flood'}
        if needW <= fh and needH <= fw:
            lw, lh = r2(fh - needW), r2(fw - needH)
            return {'frame': f'{fw} x {fh}', 'orientation': 'landscape', 'spare_w': lw, 'spare_h': lh,
                    'verdict': 'snug fit' if min(lw, lh) < 6 else 'room to flood'}
    return {'frame': None, 'orientation': 'no fit', 'spare_w': None, 'spare_h': None,
            'verdict': 'too big for standard frames (labeled)'}

def inkGrams(printW, printH, colors, prints):
    areaM2 = printW * printH / 10000
    kg = areaM2 * prints * colors / COVER * WASTE
    grams = math.floor(kg * 1000 + 0.5)
    verdict = ('a thimble - one small jar covers it' if grams < 100 else 'a small jar' if grams < 500
               else 'a 1 kg tub' if grams < 1000 else 'stock up - multiple tubs')
    return {'grams': grams, 'verdict': verdict}

def runMinutes(prints, colors, pullSec, setupMin, dryMin):
    total = setupMin * colors + prints * colors * pullSec / 60 + dryMin * (colors - 1)
    minutes = math.floor(total * 10 + 0.5) / 10
    verdict = 'quick run' if minutes <= 60 else 'an afternoon' if minutes <= 240 else 'a long session'
    return {'minutes': minutes, 'verdict': verdict}

CASES = [
  {'card':'frameFit','args':[20,28]}, {'card':'frameFit','args':[28,20]},
  {'card':'frameFit','args':[1,1]},   {'card':'frameFit','args':[24,34]},
  {'card':'frameFit','args':[25,35]}, {'card':'frameFit','args':[30,40]},
  {'card':'frameFit','args':[34,44]}, {'card':'frameFit','args':[40,60]},
  {'card':'frameFit','args':[54,64]}, {'card':'frameFit','args':[38,54]},
  {'card':'frameFit','args':[38,42]}, {'card':'frameFit','args':[10,10]},
  {'card':'frameFit','args':[0,20],'error':'positive'},
  {'card':'frameFit','args':[-3,20],'error':'positive'},
  {'card':'frameFit','args':[20,0],'error':'positive'},
  {'card':'frameFit','args':[20,-1],'error':'positive'},
  {'card':'inkGrams','args':[20,28,2,30]}, {'card':'inkGrams','args':[10,10,1,5]},
  {'card':'inkGrams','args':[50,70,1,100]},{'card':'inkGrams','args':[50,70,4,100]},
  {'card':'inkGrams','args':[20,20,1,1]},  {'card':'inkGrams','args':[30,40,3,50]},
  {'card':'inkGrams','args':[15,15,2,10]}, {'card':'inkGrams','args':[40,50,1,25]},
  {'card':'inkGrams','args':[25,35,2,40]}, {'card':'inkGrams','args':[10,15,1,75]},
  {'card':'inkGrams','args':[0,28,2,30],'error':'positive'},
  {'card':'inkGrams','args':[20,0,2,30],'error':'positive'},
  {'card':'inkGrams','args':[20,28,0,30],'error':'colors'},
  {'card':'inkGrams','args':[20,28,13,30],'error':'colors'},
  {'card':'inkGrams','args':[20,28,2,0],'error':'at least 1'},
  {'card':'inkGrams','args':[20,28,2.5,30],'error':'colors'},
  {'card':'runMinutes','args':[30,2,20,15,10]}, {'card':'runMinutes','args':[30,1,20,15,0]},
  {'card':'runMinutes','args':[50,3,25,20,15]}, {'card':'runMinutes','args':[100,2,30,15,10]},
  {'card':'runMinutes','args':[10,4,15,10,5]},  {'card':'runMinutes','args':[200,2,30,15,10]},
  {'card':'runMinutes','args':[200,2,30,15,15]},{'card':'runMinutes','args':[5,1,10,0,0]},
  {'card':'runMinutes','args':[500,4,20,20,10]},{'card':'runMinutes','args':[12,1,20,15,0]},
  {'card':'runMinutes','args':[0,2,20,15,10],'error':'at least 1'},
  {'card':'runMinutes','args':[30,0,20,15,10],'error':'colors'},
  {'card':'runMinutes','args':[30,13,20,15,10],'error':'colors'},
  {'card':'runMinutes','args':[30,2,0,15,10],'error':'positive'},
  {'card':'runMinutes','args':[30,2,20,-5,10],'error':"negative"},
  {'card':'runMinutes','args':[30,2,20,15,-1],'error':"negative"},
]

out = []
for c in CASES:
    row = {'card': c['card'], 'args': c['args']}
    if 'error' in c:
        row['error'] = c['error']
    else:
        row['expect'] = globals()[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as f:
    json.dump(out, f, indent=1)
    f.write('\n')
print('wrote', len(out), 'cases')
