# 🦊 Fox Chess Lab

A chess analysis site that runs entirely in the browser:

- **Analysis board** with Stockfish 18 (WebAssembly), game review and move ratings
- **Screenshot to position**: set up a board from a 2D chess screenshot
- **Opening explorer**: Masters and Lichess databases, with rating and speed filters
- **Repertoire map**: your openings as a branching tree, with gaps you haven't prepared highlighted
- **Studies**: line chapters and "solve, then reveal" calculation exercises

The site lives in [`docs/`](docs/) and is served by GitHub Pages.

## Sign in with Lichess

"Sign in with Lichess" uses Lichess's OAuth2 PKCE flow, which needs no app registration. The site asks for
no special permissions: it reads the opening explorer and your username. Your sign-in token is kept only in your
browser, and signing out revokes it on Lichess.

## Opening explorer

Signed out, the explorer uses a small built-in opening book (move popularity only). Signed in with Lichess, it looks
positions up live in the Lichess Masters and Lichess games databases, with results, average ratings and top games.

## Your data

Studies and repertoires are saved in your browser (localStorage) on this site. Clearing site data removes them.

## Licences

- Code in this repository: GPL-3.0 (see [LICENSE](LICENSE)).
- [Stockfish](https://github.com/official-stockfish/Stockfish) via [stockfish.js](https://github.com/nmrugg/stockfish.js): GPL-3.0.
- [chess.js](https://github.com/jhlywa/chess.js): BSD-2-Clause, loaded from jsDelivr.
- Piece sets cburnett (Colin M.L. Burnett) and Merida (Armando Hernandez Marroquin): GPL-2.0-or-later, as used on Lichess.
- Opening names: [lichess-org/chess-openings](https://github.com/lichess-org/chess-openings) (CC0).
- Opening data from the Lichess opening explorer (<https://explorer.lichess.org>).
