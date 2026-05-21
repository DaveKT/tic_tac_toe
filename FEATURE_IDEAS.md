## Sync Stats to Play Mode

Game statistics currently persist across games, which is the desired behavior within a single play mode. However, switching between play modes (computer vs. human, human vs. human, computer vs. computer) does not reset the stats, because a mode change is not treated as a new session.

Link statistics to the active play mode so that selecting a different play mode automatically clears the stats.

## Add Grid Hatch to UI

The current UI omits the classic tic-tac-toe hash grid. The spaces between cells where X's and O's are placed are rendered with padding only.

Add black lines between cells to produce the traditional hatch grid.

## Online Multiplayer

The app currently only supports local play, requiring both players to share the same device. There is no way to play against a remote opponent over a network.

Add online multiplayer support so that two players can connect over a network and play against each other in real time from separate devices.

## Dark Mode

The current UI uses a fixed light theme with no option to switch to a darker color scheme. Users who prefer lower-brightness interfaces or work in low-light environments have no alternative.

Add a dark mode toggle that switches the board, background, and text colors to a dark theme, persisting the user's preference across sessions.

## ~~Beatable Computer Option~~

~~The computer opponent was originally designed to always make the optimal move, making it unbeatable. This can reduce replay value.~~

~~Add an option for a computer opponent that is challenging but beatable.~~