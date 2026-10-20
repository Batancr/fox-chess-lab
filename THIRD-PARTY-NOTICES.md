# Third-party software

The site uses the following software, which keeps its own licence:

- **Stockfish** chess engine, as compiled to WebAssembly by stockfish.js (`docs/stockfish-18-lite-single.js` and
  `docs/stockfish-18-lite-single.wasm`, unmodified). Licensed under the GNU General Public License v3; the full text
  is in [licenses/GPL-3.0.txt](licenses/GPL-3.0.txt). Source code:
  - https://github.com/nmrugg/stockfish.js
  - https://github.com/official-stockfish/Stockfish
- **chess.js** (version 0.10.3), loaded from the jsDelivr CDN. Source and licence: https://github.com/jhlywa/chess.js
- **Atkinson Hyperlegible Next** font, by the Braille Institute and the Atkinson Hyperlegible Next Project Authors,
  carried inside `docs/index.html` (the Latin and Latin Extended files, unmodified). Licensed under the SIL Open Font
  License 1.1; the full text is in [licenses/OFL-1.1.txt](licenses/OFL-1.1.txt). Source:
  https://github.com/googlefonts/atkinson-hyperlegible-next
- Opening explorer data and sign-in come from **Lichess** (https://lichess.org) through its public API.
