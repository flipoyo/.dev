# Improve tuto 2: branch management

## Problem

In tuto 2, `pixi run cgitsync push` is refused on GitLab `main` (protected branch). This is expected behavior.
Check the consistancy with other tuto for moving simple branch experience in tuto 2



## Required change

Tuto 2 must include a branch management step before the push, so the user works on a feature branch instead of `main`.

## Commands to add to tuto 2

1. Create a branch:
   ```bash
   pixi run cgitsync branch create <name-branch>
   ```
2. List branches:
   ```bash
   pixi run cgitsync branch list
   ```
3. Switch to the branch:
   ```bash
   pixi run cgitsync branch checkout <name-branch>
   ```
4. Push from the feature branch:
   ```bash
   pixi run cgitsync push
   ```


## Check tutos consistency

Check the consistancy with other tuto for moving simple branch experience in tuto 2

## Tasks

- [ ] Add a "Branch management" section to tuto 2, before the push step.
- [ ] Explain that `main` is protected on GitLab and direct push is refused.
- [ ] Document `branch create`, `branch list`, `branch checkout`.
- [ ] Update the push step to run from the feature branch.
- [ ] Verify the full tuto 2 flow end to end.
