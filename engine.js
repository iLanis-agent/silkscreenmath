/* Silkscreen math - exact arithmetic, labeled norms.
   Labeled norms shown in the UI: 8 cm squeegee margin each side, standard frames
   25x35 / 30x40 / 40x50 / 50x70 cm, ink coverage ~9 m2 per kg (water-based, standard
   mesh), 20% waste, 20 s per pull, 15 min setup per screen, 10 min dry gap. */
(function (root) {
  'use strict';

  var MARGIN = 8;              // cm each side (labeled squeegee margin)
  var FRAMES = [[25,35],[30,40],[40,50],[50,70]];  // cm, labeled common sizes
  var COVER_M2_PER_KG = 9;     // labeled coverage norm
  var WASTE = 1.2;             // labeled 20% waste factor

  function r2(x) { return Math.round(x * 100) / 100; }
  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }

  function frameFit(imgW, imgH) {
    imgW = num(imgW, 'image width'); imgH = num(imgH, 'image height');
    if (imgW <= 0 || imgH <= 0) throw new Error('image dimensions must be positive');
    var needW = imgW + 2 * MARGIN, needH = imgH + 2 * MARGIN;
    for (var i = 0; i < FRAMES.length; i++) {
      var fw = FRAMES[i][0], fh = FRAMES[i][1];
      if (needW <= fw && needH <= fh) {
        var sw = r2(fw - needW), sh = r2(fh - needH);
        return { frame: fw + ' x ' + fh, orientation: 'portrait', spare_w: sw, spare_h: sh,
                 verdict: Math.min(sw, sh) < 6 ? 'snug fit' : 'room to flood' };
      }
      if (needW <= fh && needH <= fw) {
        var lw = r2(fh - needW), lh = r2(fw - needH);
        return { frame: fw + ' x ' + fh, orientation: 'landscape', spare_w: lw, spare_h: lh,
                 verdict: Math.min(lw, lh) < 6 ? 'snug fit' : 'room to flood' };
      }
    }
    return { frame: null, orientation: 'no fit', spare_w: null, spare_h: null,
             verdict: 'too big for standard frames (labeled)' };
  }

  function inkGrams(printW, printH, colors, prints) {
    printW = num(printW, 'print width'); printH = num(printH, 'print height');
    if (printW <= 0 || printH <= 0) throw new Error('print dimensions must be positive');
    if (!Number.isInteger(colors) || colors < 1 || colors > 12) throw new Error('colors run 1 to 12 (labeled)');
    if (!Number.isInteger(prints) || prints < 1) throw new Error('need at least 1 print');
    var areaM2 = printW * printH / 10000;
    var kg = areaM2 * prints * colors / COVER_M2_PER_KG * WASTE;
    var grams = Math.round(kg * 1000);
    var verdict = grams < 100 ? 'a thimble - one small jar covers it'
                : grams < 500 ? 'a small jar'
                : grams < 1000 ? 'a 1 kg tub'
                : 'stock up - multiple tubs';
    return { grams: grams, verdict: verdict };
  }

  function runMinutes(prints, colors, pullSec, setupMin, dryMin) {
    if (!Number.isInteger(prints) || prints < 1) throw new Error('need at least 1 print');
    if (!Number.isInteger(colors) || colors < 1 || colors > 12) throw new Error('colors run 1 to 12 (labeled)');
    pullSec = num(pullSec, 'pull seconds');
    if (pullSec <= 0) throw new Error('pull seconds must be positive');
    setupMin = num(setupMin, 'setup minutes'); dryMin = num(dryMin, 'drying minutes');
    if (setupMin < 0) throw new Error("setup minutes can't be negative");
    if (dryMin < 0) throw new Error("drying minutes can't be negative");
    var total = setupMin * colors + prints * colors * pullSec / 60 + dryMin * (colors - 1);
    var minutes = Math.round(total * 10) / 10;
    var verdict = minutes <= 60 ? 'quick run' : minutes <= 240 ? 'an afternoon' : 'a long session';
    return { minutes: minutes, verdict: verdict };
  }

  var api = { frameFit: frameFit, inkGrams: inkGrams, runMinutes: runMinutes,
              NORMS: { MARGIN: MARGIN, FRAMES: FRAMES, COVER_M2_PER_KG: COVER_M2_PER_KG, WASTE: WASTE } };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.SilkscreenMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
