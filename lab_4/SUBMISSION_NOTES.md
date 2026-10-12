# Lab 4 - VibeCoding: Fruit Slice

## Changes
- Task 1 (collision): `Fruit.intersects_segment()` tests the blade segment between the previous and current mouse positions against the fruit circle, so fast swipes register.
- Task 2 (game over): in-game overlay with reason, final score; waits for input.
- Task 3 (replay): choose Easy / Medium / Hard (keys 1/2/3 or click) or Quit (Q / Esc / click). Difficulty changes spawn interval and bomb chance.
- Task 4 (sound): slice, bomb and game-over sounds generated in code (`game/sounds.py`), no audio files; falls back silently if no audio device.
- Also: blade trail now fades when the mouse stops; no slicing after game over; lives never display below 0.

## To add before pushing
- before.mp4 / after.mp4 (10 s each)
- Chat history export (PDF/doc)
