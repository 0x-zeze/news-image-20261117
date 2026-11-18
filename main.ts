// news-image-20261117 — "The World in One Day", Tuesday 17 November 2026.
// Node 22, standard library only. The entry image is drawn by
// generate-image.py (Pillow, offline) and shipped beside this file as
// entry.png; this program copies it, byte for byte, to the output
// directory the grader provides. No network, no randomness, so two runs
// always write the same bytes.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
// Guard: the copy must be byte-identical in size, or the run is wrong.
if (statSync(src).size !== statSync(dest).size) {
  throw new Error('entry.png copy size mismatch');
}
