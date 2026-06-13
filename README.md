# ft_pomodoro

A minimalist, floating session timer tailored for 42 Network cluster environments. It rides on top of your coding workspace (Neovim, VS Code, Browser) to keep your focus sessions in check, automatically invoking custom lock scripts like `ft_lock` if you ignore the break threshold.

## Features

- **Floating HUD:** Tiny, zero-distraction clock window forced to stay on top (`-topmost`).
- **Toggleable Controls:** Advanced parameters hide completely until you click `⚙ Config`.
- **Custom Lock Command:** Swap `ft_lock` for any terminal instruction or custom script on the fly.
- **Dynamic Quick Scales:** Instantly switch between 15m, 30m, 45m, or 60m focus blocks.
- **On-the-Fly Pausing:** Freeze your session seamlessly when walking away for a quick break or peer-evaluation.

## Installation & Requirements

The project uses standard library bindings and requires Python 3 with `tkinter` support.

```bash
git clone [https://github.com/laghzal49/ft_pomodoro.git](https://github.com/laghzal49/ft_pomodoro.git)
cd ft_pomodoro