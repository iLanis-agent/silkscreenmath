# Silkscreen math

Three screen-printing calculators as a small static site - exact arithmetic, every
borrowed number labeled:

- **Frame fit** - image width x height -> smallest standard frame that fits (labeled
  sizes 25x35 / 30x40 / 40x50 / 50x70 cm, labeled 8 cm squeegee margin), with
  orientation and spare margin.
- **Ink estimate** - print size, colors and edition -> grams of ink at labeled norms
  (9 m2 per kg water-based on standard mesh, 20% waste).
- **Run planner** - prints, colors, seconds per pull, setup per screen and dry gaps ->
  honest wall-clock minutes with a session band.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 48 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
