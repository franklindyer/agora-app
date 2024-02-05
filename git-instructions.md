# Repo setup
You can set up a repo however you'd like, but I put my method here just for posterity.
Make and move to folder where you want the repo to be:
```
cd <REPO-FOLDER>
```

Initialize an empty git repo with no ties to any remote:
```
git init .
```

Add the remote repo as a "remote" head from the ssh link you get from "clone" on github:
```
git remote add origin <SSH-LINK-FROM-GITHUB-REPO>
```

Then, follow the steps below for fetch and reset.

# Update local branch(es) to remote
"Fetch" the changes from the remote. This will make git *aware* of changes that have happened on the remote, but it will *not apply* any changes yet:
```
git fetch --all -p
```
Now, decide how you want to update your local code.

* To *overwrite* your local changes (except for stashed changes and untracked files):
  ```
  git reset --hard origin/<BRANCH-NAME-ON-REMOTE>
  ```

* To incorporate *uncommited* changes to an updated remote branch, you can "stash" your changes, reset to the remote branch, and then unstash your changes:
  ```
  git stash
  git fetch --all -p
  git reset --hard origin/<BRANCH>
  git stash pop
  ```
  When you `pop`, you may run into merge conflicts if the changes you've stashed conflict with whatever changes were made to the remote branch.

* To incorporate *committed* changes to a new base branch, we need to rebase:
  ```
  git fetch --all -p
  git rebase -i origin/<BRANCH>
  ```
  Using the option `-i` is performing an interactive rebase so you can see exactly what's going on. This is the preferred way to rebase so you can sanity check what's happeneing. 

  This will open up a file in your default text editor with all of the commits you've made on your local branch. There are many powerful things you can do with a rebase, but the most important features are these:
  * `pick` prepended to a commit (default) will keep that commit in your rebase, unless the remote also has that commit (in which case it will drop it because it is redundant).
  * deleting a line will *SKIP* that commit during your rebase, and those changes will be *DELETED*! So don't remove any lines that you want to keep.
  * However, deleting ALL the lines will abort the rebase - this is useful if you realize you want to back out, just delete all the lines (lines starting with `#` are ignored already) and the rebase will be aborted.
  * _IMPORTANT NOTE_ just leaving the file (`:q!`) will NOT abort the rebase. If you leave the file unchanged, the rebase will continue as if you exited with intent (`:wq`) becuase you are *changing* the file as opposed to *creating* it.
 
  Inside the rebase file:
  ```
  git pick <HASH> <COMMIT-MESSAGE> # Oldest commit
  ...
  git pick <HASH> <COMMIT-MESSAGE> # Newest commit
  ```
  
  `pick` all the lines you want to keep, delete the lines you want to skip, and then save and close the rebase file. If there were merge conflicts, you will see that now, and you can run `git status` to see exactly which files have conflicts (they will say `both modified`).
  
  When you fix a merge conflict in a file, you then need to let git know that you've fixed it, then you can continue with the rebase.
  ```
  git add <FILENAME1> <FILENAME2> ... <FILENAMEn>
  git rebase --continue
  ```
  When there are no more merge conflicts (which may happen the first time), you will see a message saying you successfully rebased your branch.

  To push to a branch where you have rebased, you must use `--force`. If you are pushing a branch you've rebased to the remote for the first time (e.g., there is not a branch of the same name existing on the remote), then you don't have to force push.
