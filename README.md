# Data Science & Agentic AI Programme

An 8-week programme from machine learning to multi-agent AI, with a Week 0 onboarding sprint.

- **Repository:** <https://github.com/samuelts96/ds-october-2026>
- **Syllabus:** [syllabus/DS_Agentic_AI_Syllabus.pdf](syllabus/DS_Agentic_AI_Syllabus.pdf)
- **Dates:** Week 0 Wed 30 Sep - Fri 2 Oct 2026, then Weeks 1-8 Mon 5 Oct - Fri 27 Nov 2026
- **Progress tracking:** the DS October Trello board (one card per person per week)

| Day | What happens |
|---|---|
| Every day, 09:15 | Scrum call: what you did, what you're doing today, blockers |
| Monday | Prep day |
| Tuesday | Presentations of the previous week's work (from Week 2) |
| Wednesday - Friday | Teaching and labs |

---

# Git guide

Git tracks changes to your files. GitHub hosts Git repositories online so you can share and back them up.

## 1. One-time setup

Install Git from <https://git-scm.com/downloads> and create an account at <https://github.com>, then tell Git who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"   # the email on your GitHub account
git config --global init.defaultBranch main
git config --global pull.rebase false               # `git pull` merges (the simplest default)
```

Check it with `git config --global --list`.

## 2. Key ideas

| Term | Meaning |
|---|---|
| **Repository (repo)** | A project folder whose history Git tracks |
| **Working directory** | The files you are editing right now |
| **Staging area** | The changes you've chosen to include in the next commit (`git add`) |
| **Commit** | A saved snapshot with a message |
| **Branch** | An independent line of work; `main` is the default |
| **Remote** | A copy of the repo elsewhere, usually on GitHub. `origin` = your copy |
| **Fork** | Your own GitHub copy of someone else's repo |
| **Upstream** | The original repo you forked from |

```
edit files  ->  git add  ->  git commit  ->  git push
(working)       (staged)     (local history)  (GitHub)
```

## 3. Week 0 essentials

These are the commands we use from day one.

### Fork and clone

1. Open <https://github.com/samuelts96/ds-october-2026> and click **Fork** to make your own copy.
2. Clone **your fork** to your laptop:

```bash
git clone https://github.com/<your-username>/ds-october-2026.git
cd ds-october-2026
```

### Create a new branch

Never work directly on `main`. Create a branch for each piece of work:

```bash
git checkout -b week0/<your-name>     # create the branch and switch to it
git branch                            # list branches; * marks the current one
```

(`git switch -c <branch>` is the newer equivalent of `git checkout -b <branch>`.)

### Add, commit, push

```bash
git status                            # see what changed
git add .                             # stage every change in this folder
git commit -m "Add Week 0 EDA notebook"
git push -u origin week0/<your-name>  # first push of a new branch
git push                              # later pushes on the same branch
```

`-u` links your local branch to the one on GitHub, so later you can just run `git push` and `git pull`.

## 4. Everyday commands

### Look before you act

```bash
git status                  # what's changed, staged, or untracked
git diff                    # unstaged changes
git diff --staged           # staged changes (what will be committed)
git log --oneline --graph   # compact history
```

### Staging

```bash
git add file.py             # stage one file
git add .                   # stage everything in the current folder
git restore --staged file.py  # unstage (keeps your edits)
git restore file.py         # discard unstaged edits to a file (can't be undone)
```

### Pull and fetch

```bash
git pull                    # fetch from GitHub and merge into your current branch
git fetch                   # download new commits without changing your files
```

Pull before you start work each day, and before you push.

### Switching branches

```bash
git switch main             # move to an existing branch
git switch -c feature/x     # create and move to a new branch
git branch -d feature/x     # delete a branch that has been merged
```

Commit or stash your changes before switching.

### Stash (park unfinished work)

```bash
git stash                   # put uncommitted changes aside
git stash list
git stash pop               # bring them back
```

## 5. Merge and rebase

Both bring the changes from one branch into another. They differ in the history they leave behind.

### Merge

```bash
git switch main
git pull
git merge feature/x
```

This keeps both histories and adds a **merge commit**. It is safe on shared branches because it never rewrites existing commits.

### Rebase

```bash
git switch feature/x
git fetch origin
git rebase origin/main
```

This **replays your commits on top of** the latest `main`, giving a straight-line history. It rewrites your branch's commits, so:

- Only rebase branches that **only you** work on.
- After rebasing a branch you had already pushed, you need `git push --force-with-lease`. Never force-push `main` or a shared branch.

| | Merge | Rebase |
|---|---|---|
| History | Keeps every branch and adds a merge commit | Straight line, no merge commit |
| Rewrites commits | No | Yes |
| Safe on shared branches | Yes | No; use it on your own branches only |
| Typical use | Bringing a finished feature into `main` | Updating your feature branch with the latest `main` |

### Merge conflicts

A conflict happens when two branches change the same lines. Git marks them in the file:

```
<<<<<<< HEAD
your version
=======
their version
>>>>>>> feature/x
```

1. Edit the file to keep the right content and delete the markers.
2. `git add <file>`
3. Finish with `git commit` (merge) or `git rebase --continue` (rebase).

To give up and go back: `git merge --abort` or `git rebase --abort`.

## 6. Keeping your fork up to date

Your fork doesn't update itself when the original repo changes. Add the original as `upstream` once:

```bash
git remote add upstream https://github.com/samuelts96/ds-october-2026.git
git remote -v               # origin = your fork, upstream = the original
```

Then, whenever there's new course material:

```bash
git switch main
git fetch upstream
git merge upstream/main     # or: git rebase upstream/main
git push origin main
```

You can also click **Sync fork** on your fork's GitHub page.

## 7. Pull requests

A pull request (PR) asks for your branch to be merged, and it's where reviews happen.

1. Push your branch: `git push -u origin <branch>`.
2. On GitHub, click **Compare & pull request**.
3. Write a clear title and description, then request a review.
4. Push more commits to the same branch to update the PR.

## 8. Undoing things

| Situation | Command |
|---|---|
| Fix the message of your last commit (not pushed yet) | `git commit --amend -m "Better message"` |
| Add a forgotten file to your last commit (not pushed yet) | `git add file && git commit --amend --no-edit` |
| Undo a commit that is already pushed | `git revert <commit>` (adds a new commit that reverses it) |
| Undo local commits but keep the changes | `git reset --soft HEAD~1` |
| Throw away all local changes (can't be undone) | `git reset --hard HEAD` |

Prefer `revert` for anything already pushed.

## 9. Good practice

- **Commit small and often.** One logical change per commit.
- **Write clear messages** in the imperative: `Add churn model evaluation`, not `stuff` or `changes`.
- **One branch per task**, named clearly: `week3/text-classifier`, `group-a/rag-pipeline`.
- **Pull before you push**, and before you start work each day.
- **Check `git status` and `git diff`** before every commit.
- **Never commit secrets:** API keys, passwords or `.env` files. Add them to `.gitignore`.
- **Don't commit generated or large files:** virtual environments (`.venv/`), `__pycache__/`, large datasets or model files.
- **Never force-push `main`** or a branch someone else is using.

A starter `.gitignore` for Python projects:

```
.venv/
__pycache__/
.ipynb_checkpoints/
.env
*.pyc
data/raw/
```

## 10. Cheat sheet

| Command | What it does |
|---|---|
| `git clone <url>` | Copy a repo to your laptop |
| `git status` | Show what's changed |
| `git add .` | Stage all changes |
| `git commit -m "msg"` | Save a snapshot |
| `git push` | Upload commits to GitHub |
| `git pull` | Download and merge commits from GitHub |
| `git fetch` | Download commits without merging |
| `git checkout -b <branch>` / `git switch -c <branch>` | Create and switch to a branch |
| `git switch <branch>` | Switch branch |
| `git merge <branch>` | Merge a branch into the current one |
| `git rebase <branch>` | Replay your commits on top of another branch |
| `git log --oneline` | Show history |
| `git diff` | Show unstaged changes |
| `git stash` / `git stash pop` | Park and restore unfinished work |
| `git revert <commit>` | Safely undo a pushed commit |
| `git remote -v` | Show remotes |
