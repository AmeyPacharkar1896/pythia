# 🤝 Hey! Want to help make Pythia better?

First off, thanks for even looking at this file. Pythia is a project I'm building to push the limits of what a "filesystem" can do with AI, and I’d love to have more brains working on it.

Since I'm trying to keep the code clean and easy to read (especially for my own sanity!), here are a few "vibes" I try to stick to when writing code here.

### 🛠️ How we work
- **Don't break `main`:** Try not to push directly to the main branch. Create a new branch for whatever you're working on (like `feature/cool-image-gen`) and open a Pull Request. It makes it way easier to see what's changing.
- **Talk to me:** If you find a bug, just open an issue and tell me what happened. You don't need a fancy report—just tell me how you broke it!

### 📜 The "Clean Code" Vibes
Since we just spent a lot of time refactoring this to look professional, let's keep it that way:
- **Use the Config:** If you have a setting (like a new file extension or a timeout), put it in `src/config.py`. No "magic numbers" in the middle of the code, please!
- **No `print()` allowed:** We use a cool colored logger now. Use `logger.info()` or `logger.error()` instead of printing. It makes the terminal look like a cyberpunk dashboard.
- **Type Hints:** I’m using type hints (like `name: str`) for everything. It helps VS Code help us, so try to keep that going.
- **Prompts:** If you're teaching the "Brain" a new trick, put the text template in `src/prompts.py` so the logic stays separate from the talk.

### 📂 Keep the docs fresh
If you add a new feature, just spend a minute updating the `docs/USAGE.md`. I want people to actually know how to use the cool stuff we build!

---

That’s basically it. If you have a wild idea for v3.0 or beyond, just open a PR and let's talk about it! 🚀