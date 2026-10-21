# Fox Chess Lab: changelog

A dated record of what was added. Dates are when each change was saved in Fox Chess Lab's source repository.
The site is at https://batancr.github.io/fox-chess-lab/.

## 2026-10-21
- Install Fox Chess Lab as an app (Install app in the header, or Add to Home Screen on iPhone). It opens without a
  connection: your saved work, the analysis board, the built-in book, and the engine once you've used it.
  Long-press the icon for shortcuts to Repertoire, Studies, Opponent prep and Guess the eval.

## 2026-10-20
- New font, Atkinson Hyperlegible Next, built into the page (nothing is loaded from Google any more).
- One corner radius across cards, buttons, inputs and panels.
- Grey placeholders while the explorer, your games, an opponent's games, your studies and Community posts load.

## 2026-10-12
- Studies: **+ Game analysis** imports a game from a pasted PGN or a .pgn file (one game or all of them), with the
  option to keep only the moves played and remove comments and symbols. Clock times and engine notes are always
  removed. The players, event and result show with the chapter. "+ Line chapter" is now "+ Chapter".

## 2026-10-11
- Convert the win: positions from recent master games (no sign-in needed, or your own PGN file), including only the
  ones where the win slipped; and type your own minimum advantage, e.g. +2.5.
- Guess the eval: the board faces whoever is to move.
- Opponent prep: says how many of their games reach your repertoire, and explains when their games never do, instead of
  showing the same line twice.
- Guided tour: a walk through every part of the site with example data, from **? Tour** in the header.
- Click counts: which tabs and buttons get used, counted anonymously with GoatCounter (no cookies, no personal data).
- Signing in with Lichess adds your username to the site's sign-in list (only the days you visit); said next to
  every sign-in button.
- Safety: the page now runs only its own scripts (each checked by its fingerprint), and won't run inside another
  site's frame.

## 2026-10-09
- FIDE players in Opponent prep: find a player by name or FIDE ID and see their over-the-board openings, likely line
  against your repertoire, gaps and games (events broadcast on Lichess since 2020).
- Link to ChessQ for photos of real boards.

## 2026-10-07
- Convert the win gets its own tab; new Guess the eval game.
- Low-confidence labels on win rates, "The bottom line" in game review, difficulty levels for Convert the win,
  link previews and Add to Home Screen.
- Build a repertoire from any player's games (Lichess username or PGN file).

## 2026-10-06
- My games, Opponent prep and Convert the win; move and position symbols (!, ?!, ± …).
- Sync across devices with a Lichess sign-in; the engine loads on first use.
- Novelty finder, master games study, marks for moves added from imports.

## 2026-10-04
- Split a section by move; download the repertoire tree.

## 2026-10-03
- Repertoire folders, study library and difficult calculation exercises.
- Repertoire builder, saved trees with depth estimates, adjustable board sizes, full-screen tree.
- Import options, faster big repertoires, safer saving.

## 2026-10-02
- First version: analysis board with Stockfish, opening explorer, repertoire map, studies.
- Import studies from Lichess, strong and weak points, PGN export, example mode, backup and restore.
- Share links and the Community tab.
- Game review with Lichess's own move-rating and accuracy formulas.
