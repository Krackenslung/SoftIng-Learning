---
title: Merging
domain: git
section: 08
category: daily-use
difficulty: intermediate
danger: medium
tags:
  - git/branching
  - git/merging
commands:
  - git merge
  - git mergetool
  - git rerere
related:
  - "[[Git - Rebase]]"
  - "[[Git - Branching]]"
  - "[[Bridge - PRs vs Merge]]"
sources:
  - https://git-scm.com/docs/git-merge
  - https://git-scm.com/docs/git-mergetool
  - https://git-scm.com/docs/git-rerere
  - https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
  - https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging
  - https://github.blog/open-source/git/highlights-from-git-2-34/
  - https://git-scm.com/docs/merge-strategies
updated: 2026-08-14
---

# Merging


## Fast-forward vs. three-way

**Fast-forward** — the target branch is a direct ancestor of the source, so Git
just slides the pointer forward. No merge commit.

```
before:  A───B  (main)          after:  A───B───C───D  (main, feature)
              \                                  
               C───D  (feature)
```

**Three-way merge** — both branches have new commits. Git finds the merge base
(common ancestor) and creates a merge commit with two parents.

```
        A───B───E  (main)              A───B───E───M  (main)
             \                              \     /
              C───D  (feature)               C───D
```

## Commands

```bash
git switch main
git merge feature
git merge --no-ff feature        # always create a merge commit
git merge --ff-only feature      # fail unless it's a clean fast-forward
git merge --squash feature       # combine all changes into ONE staged change
git merge --abort                # bail out mid-conflict
git merge -m "Custom message" feature
git merge --no-commit feature    # stage the merge, let you inspect first
```

`--no-ff` preserves the fact that a feature branch existed — useful when your
review process is per-branch. `--ff-only` is the right default for pulling.

## Conflicts

A conflict occurs when both sides changed the same region of the same file. Git
writes markers into the file:

```
<<<<<<< HEAD
the version on your current branch
=======
the version from the branch being merged
>>>>>>> feature
```

Workflow:

```bash
git status                       # lists "Unmerged paths"
git diff                         # shows only conflicts
# edit files, remove ALL markers
git add resolved-file.txt
git commit                       # message is pre-filled
```

Helpful during a conflict:

```bash
git diff --ours / --theirs / --base
git checkout --ours file         # take your side wholesale
git checkout --theirs file       # take their side wholesale
git merge --abort
git log --merge -p file          # commits touching the conflicted region
```

⚠️ During a **rebase**, "ours" and "theirs" are swapped relative to intuition:
"ours" is the branch you're rebasing *onto*, "theirs" is your commits.

## Merge strategies

Since Git 2.34 the default strategy is **ort** ("Ostensibly Recursive's Twin"),
which replaced `recursive`. It's faster and handles renames better.

```bash
git merge -s ort feature                        # default
git merge -X ours feature                       # prefer our side in conflicts
git merge -X theirs feature                     # prefer their side
git merge -X ignore-space-change feature
git merge -s ours feature                       # ⚠️ discard their changes entirely,
                                                #    keep the merge record
```

Note the difference: `-X ours` is a conflict *tiebreaker*; `-s ours` throws away
the other branch's content.

## Merge tools & rerere

```bash
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
git mergetool

git config --global merge.conflictStyle zdiff3   # shows the ORIGINAL too
```

`zdiff3` adds a `|||||||` section showing the common ancestor's version. It makes
conflicts dramatically easier to reason about — turn it on.

**rerere** ("reuse recorded resolution") records how you resolved a conflict and
replays it automatically next time the same conflict appears. Essential for long-
lived branches and repeated rebases.

```bash
git config --global rerere.enabled true
```

---

## Related

- [[Git - Rebase]]
- [[Git - Branching]]
- [[Bridge - PRs vs Merge]]

## Sources

- <https://git-scm.com/docs/git-merge>
- <https://git-scm.com/docs/git-mergetool>
- <https://git-scm.com/docs/git-rerere>
- <https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging>
- <https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging>
- <https://github.blog/open-source/git/highlights-from-git-2-34/>
- <https://git-scm.com/docs/merge-strategies>
