# Comprehensive Git Cheatsheet

## Table of Contents
1. [Git Setup and Configuration](#git-setup-and-configuration)
2. [Creating and Cloning Repositories](#creating-and-cloning-repositories)
3. [Basic Commands](#basic-commands)
4. [Working with Branches](#working-with-branches)
5. [Stashing Changes](#stashing-changes)
6. [Inspecting a Repository](#inspecting-a-repository)
7. [Undoing Changes](#undoing-changes)
8. [Rewriting History](#rewriting-history)
9. [Working with Remotes](#working-with-remotes)
10. [Tagging](#tagging)
11. [Submodules](#submodules)
12. [Advanced Operations](#advanced-operations)
13. [Git Workflows](#git-workflows)
14. [Git Hooks](#git-hooks)
15. [Troubleshooting](#troubleshooting)

## Git Setup and Configuration

Git needs to be installed and configured before you can start using it. This section covers how to install Git on different operating systems and set up your identity and preferences. Proper configuration ensures your commits are correctly attributed and Git behaves according to your workflow needs.

### Installation
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install git

# macOS
brew install git  # Using Homebrew
# OR
# Download from https://git-scm.com/download/mac

# Windows
# Download from https://git-scm.com/download/win
```

### First-time Git Configuration
```bash
# Set your user name
git config --global user.name "Your Name"

# Set your email address
git config --global user.email "your.email@example.com"

# Set default editor (e.g., VS Code)
git config --global core.editor "code --wait"

# Set default branch name for new repositories
git config --global init.defaultBranch main
```

### Configuration Levels
```bash
git config --system  # System-wide configuration (/etc/gitconfig)
git config --global  # User-specific configuration (~/.gitconfig)
git config --local   # Repository-specific configuration (.git/config)
```

### View Configuration
```bash
# List all configurations
git config --list

# View specific configuration
git config user.name
```

### Aliases
```bash
# Create shortcuts for common commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

## Creating and Cloning Repositories

When starting a new project or working with existing code, you'll need to either create a new Git repository or clone an existing one. These commands help you initialize a fresh repository or create a local copy of a remote repository to work with.

### Initialize a New Repository
```bash
# Create a new repository in the current directory
git init

# With specific branch name
git init --initial-branch=main
# OR
git init -b main
```

### Clone an Existing Repository
```bash
# Basic clone
git clone https://github.com/username/repository.git

# Clone to a specific directory
git clone https://github.com/username/repository.git my-project

# Clone a specific branch
git clone -b branch-name https://github.com/username/repository.git

# Shallow clone (limit history to save space)
git clone --depth=1 https://github.com/username/repository.git

# Clone with submodules
git clone --recurse-submodules https://github.com/username/repository.git
```

## Basic Commands

These are the fundamental Git commands you'll use daily. They help you track changes, stage files for commits, and record snapshots of your project. Understanding these commands is essential for any Git workflow, as they form the core of version control operations.

### Checking Status
```bash
# Show working tree status
git status

# Short format status
git status -s
```

### Staging Files
```bash
# Add a specific file
git add file.txt

# Add multiple files
git add file1.txt file2.txt

# Add all files in the current directory
git add .

# Add all files with a specific extension
git add *.txt

# Add all modified files (not new ones)
git add -u

# Interactive add
git add -i

# Add portions of files
git add -p
```

### Committing Changes
```bash
# Commit staged changes
git commit -m "Your commit message"

# Amend the previous commit
git commit --amend

# Add all changes and commit
git commit -a -m "Your commit message"

# Create an empty commit
git commit --allow-empty -m "Empty commit"
```

### Removing Files
```bash
# Remove from working directory and staging area
git rm file.txt

# Remove from staging area only (keep in working directory)
git rm --cached file.txt

# Remove multiple files
git rm file1.txt file2.txt

# Remove using pattern
git rm *.txt
```

### Moving/Renaming Files
```bash
# Rename a file
git mv old_filename.txt new_filename.txt

# Move a file to a directory
git mv file.txt directory/
```

### .gitignore
Example .gitignore file:
```
# Ignore compiled files
*.o
*.out
*.exe

# Ignore logs and databases
*.log
*.sql
*.sqlite

# Ignore OS generated files
.DS_Store
Thumbs.db

# Ignore node modules
node_modules/

# Ignore build directories
build/
dist/

# Ignore environment files
.env
.env.local

# Ignore IDE files
.idea/
.vscode/
*.swp
```

To ignore a file that is already tracked:
```bash
git rm --cached file.txt
# Then add it to .gitignore
```

## Working with Branches

Branches allow parallel development by creating separate lines of work. They're essential for feature development, bug fixes, and collaboration. This section covers how to create, switch between, compare, and merge branches, which are crucial skills for efficient Git workflows and team collaboration.

### Listing Branches
```bash
# List local branches
git branch

# List remote branches
git branch -r

# List all branches (local and remote)
git branch -a

# Show last commit on each branch
git branch -v

# Show branches that have been merged into the current branch
git branch --merged

# Show branches that have not been merged
git branch --no-merged
```

### Creating Branches
```bash
# Create a new branch
git branch branch-name

# Create and switch to new branch
git checkout -b branch-name

# Create based on another branch
git checkout -b branch-name source-branch

# Create based on a specific commit
git checkout -b branch-name commit-hash
```

### Switching Branches
```bash
# Switch to an existing branch
git checkout branch-name

# Switch to the previous branch
git checkout -

# Switch with git switch (Git 2.23+)
git switch branch-name

# Create and switch with git switch
git switch -c branch-name
```

### Comparing Branches
```bash
# Compare two branches
git diff branch1..branch2

# Compare specific files between branches
git diff branch1..branch2 -- file.txt

# Show branch pointing commits
git show-branch
```

### Merging Branches
```bash
# Merge a branch into the current branch
git merge branch-name

# No-fast-forward merge (always create a merge commit)
git merge --no-ff branch-name

# Fast-forward only if possible, otherwise abort
git merge --ff-only branch-name

# Squash all commits into a single one
git merge --squash branch-name
```

### Rebasing
```bash
# Rebase current branch onto another branch
git rebase branch-name

# Interactive rebase
git rebase -i branch-name

# Interactive rebase for last n commits
git rebase -i HEAD~3
```

### Cherry-picking
```bash
# Apply a specific commit to the current branch
git cherry-pick commit-hash

# Cherry-pick without committing
git cherry-pick -n commit-hash

# Cherry-pick a range of commits
git cherry-pick start-commit..end-commit
```

### Deleting Branches
```bash
# Delete a branch (after it's merged)
git branch -d branch-name

# Force delete a branch (even if not merged)
git branch -D branch-name

# Delete a remote branch
git push origin --delete branch-name
# OR
git push origin :branch-name
```

## Stashing Changes

Stashing allows you to temporarily save changes that you're not ready to commit. This is useful when you need to switch branches, pull updates, or address an urgent issue without committing incomplete work. Stashes are stored in a stack, so you can apply them later or on different branches.

### Basic Stashing
```bash
# Stash changes
git stash

# Stash with a message
git stash save "Your stash message"

# Stash including untracked files
git stash -u
# OR
git stash --include-untracked

# Stash specific files
git stash push file1.txt file2.txt
```

### Managing Stashes
```bash
# List all stashes
git stash list

# Show stash content
git stash show stash@{0}

# Show stash diff
git stash show -p stash@{0}

# Apply a stash (keep it in the stash list)
git stash apply stash@{0}

# Apply and remove the latest stash
git stash pop

# Apply and remove a specific stash
git stash pop stash@{1}

# Remove a specific stash
git stash drop stash@{1}

# Remove all stashes
git stash clear
```

### Create Branch from Stash
```bash
# Create a new branch with the stashed changes
git stash branch branch-name stash@{0}
```

## Inspecting a Repository

These commands help you understand what's happening in your repository. They allow you to view commit history, examine changes between commits, see who modified specific code, and track reference changes. These tools are invaluable for code review, debugging, and understanding project evolution.

### View History
```bash
# Basic log
git log

# Show commits in one line
git log --oneline

# Show graph of branches
git log --graph

# Show commits from a specific author
git log --author="Author Name"

# Show commits in a date range
git log --since="2023-01-01" --until="2023-12-31"

# Show commits with full diff
git log -p

# Show log with stats
git log --stat

# Customize log format
git log --pretty=format:"%h - %an, %ar : %s"

# Filter commits by message content
git log --grep="bug fix"

# Filter commits by file
git log -- path/to/file.txt

# Show merged commits
git log --merges
```

### Show Changes
```bash
# Show changes between working tree and index
git diff

# Show changes between index and last commit
git diff --staged
# OR
git diff --cached

# Show changes between two commits
git diff commit1..commit2

# Show changes for a specific file
git diff -- path/to/file.txt

# Show changes with word diff
git diff --word-diff

# Show changes between branches
git diff branch1..branch2
```

### Blame
```bash
# Show who changed each line in a file
git blame file.txt

# Show specific line range
git blame -L 10,20 file.txt

# Ignore whitespace changes
git blame -w file.txt

# Show the commit that last modified a line
git blame -l file.txt
```

### Analyzing Objects
```bash
# Show commit details
git show commit-hash

# Show commit with diff
git show --stat commit-hash

# Show a file from a specific commit
git show commit-hash:path/to/file.txt

# List repository objects
git cat-file -t object-hash  # Show type
git cat-file -p object-hash  # Show content
```

### Reflog
```bash
# Show reference logs
git reflog

# Show reflog for a specific branch
git reflog show branch-name

# Limit reflog entries
git reflog -n 10
```

## Undoing Changes

Everyone makes mistakes, and Git offers several ways to undo changes at different stages. These commands help you discard uncommitted changes, unstage files, revert commits, or reset to previous states. Understanding these commands helps you recover from errors without losing work.

### Checkout Files
```bash
# Discard changes in working directory
git checkout -- file.txt

# Checkout a file from a specific commit
git checkout commit-hash -- file.txt
```

### Reset
```bash
# Unstage a file
git reset file.txt

# Undo the last commit but keep changes staged
git reset --soft HEAD^

# Undo the last commit and unstage changes
git reset HEAD^

# Undo the last commit and discard changes
git reset --hard HEAD^

# Reset to a specific commit
git reset --hard commit-hash
```

### Revert
```bash
# Create a new commit that undoes a previous commit
git revert commit-hash

# Revert multiple commits
git revert start-hash..end-hash

# Revert without automatically committing
git revert -n commit-hash
```

### Restore (Git 2.23+)
```bash
# Restore working tree file
git restore file.txt

# Restore a file from a specific commit
git restore --source=commit-hash file.txt

# Unstage a file
git restore --staged file.txt
```

### Clean
```bash
# Remove untracked files (show what will be removed first)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove untracked and ignored files
git clean -fdx
```

## Rewriting History

Sometimes you need to clean up your commit history before sharing it. These commands let you edit, reorder, combine, or split commits to create a more logical and coherent history. Use these with caution on shared branches, as they change Git history and can cause conflicts for collaborators.

### Interactive Rebase
```bash
# Start interactive rebase for last n commits
git rebase -i HEAD~3

# Common rebase commands:
# - p, pick = use commit
# - r, reword = use commit, but edit the commit message
# - e, edit = use commit, but stop for amending
# - s, squash = use commit, but meld into previous commit
# - f, fixup = like "squash", but discard this commit's log message
# - d, drop = remove commit
```

### Squashing Commits
```bash
# Squash last 3 commits interactively
git rebase -i HEAD~3
# Then change "pick" to "squash" for the commits you want to combine
```

### Splitting Commits
```bash
# Split a commit
git rebase -i HEAD~3
# Change "pick" to "edit" for the commit you want to split
# Reset to the previous commit
git reset HEAD^
# Stage and commit parts separately
git add part-of-file.txt
git commit -m "First part"
git add another-part.txt
git commit -m "Second part"
# Continue rebase
git rebase --continue
```

### Reordering Commits
```bash
# Start interactive rebase
git rebase -i HEAD~3
# Reorder the lines in the editor, then save and exit
```

### Filter-branch (Advanced)
```bash
# Remove a file from all commits
git filter-branch --tree-filter 'rm -f passwords.txt' HEAD

# Change author/email in all commits
git filter-branch --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "old@example.com" ]
then
    export GIT_AUTHOR_EMAIL="new@example.com"
    export GIT_AUTHOR_NAME="New Name"
fi
' HEAD
```

## Working with Remotes

Remote repositories enable collaboration and provide backup for your code. These commands help you connect to, fetch from, and push to remote repositories like those on GitHub, GitLab, or Bitbucket. They're essential for team collaboration and for maintaining synchronized copies of your codebase.

### Managing Remotes
```bash
# List remotes
git remote

# List remotes with URLs
git remote -v

# Add a remote
git remote add origin https://github.com/username/repo.git

# Change remote URL
git remote set-url origin https://github.com/username/new-repo.git

# Rename a remote
git remote rename origin upstream

# Remove a remote
git remote remove upstream

# Show information about a remote
git remote show origin
```

### Fetching and Pulling
```bash
# Fetch from remote
git fetch origin

# Fetch all remotes
git fetch --all

# Fetch a specific branch
git fetch origin branch-name

# Pull from remote (fetch + merge)
git pull origin branch-name

# Pull with rebase instead of merge
git pull --rebase origin branch-name

# Pull all branches
git pull --all
```

### Pushing
```bash
# Push to remote
git push origin branch-name

# Push and set upstream
git push -u origin branch-name

# Force push (use with caution!)
git push --force origin branch-name

# Push all branches
git push --all origin

# Push all tags
git push --tags origin

# Delete a remote branch
git push origin --delete branch-name
```

### Tracking Branches
```bash
# Set a local branch to track a remote branch
git branch --track branch-name origin/branch-name

# Change tracking branch
git branch -u origin/branch-name

# Show tracking branches
git branch -vv
```

## Tagging

Tags provide a way to mark specific points in your repository's history, typically for release versions. Unlike branches, tags don't change once created (unless forced). They're useful for marking release points (v1.0.0, v2.0.0) and for creating permanent references to important commits.

### Creating Tags
```bash
# Create a lightweight tag
git tag v1.0.0

# Create an annotated tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Create a tag for a specific commit
git tag -a v1.0.0 -m "Version 1.0.0" commit-hash
```

### Listing Tags
```bash
# List all tags
git tag

# List tags matching a pattern
git tag -l "v1.0.*"

# Show tag details
git show v1.0.0
```

### Deleting Tags
```bash
# Delete a local tag
git tag -d v1.0.0

# Delete a remote tag
git push origin --delete v1.0.0
# OR
git push origin :refs/tags/v1.0.0
```

### Pushing and Fetching Tags
```bash
# Push a specific tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# Fetch all tags
git fetch --tags
```

### Checking Out Tags
```bash
# Checkout a tag (detached HEAD state)
git checkout v1.0.0

# Create a branch from a tag
git checkout -b branch-name v1.0.0
```

## Submodules

Submodules allow you to include other Git repositories within your project. They're useful for incorporating third-party libraries or splitting large projects into smaller, manageable pieces. These commands help you add, update, and manage nested repositories within your main project.

### Adding Submodules
```bash
# Add a submodule
git submodule add https://github.com/username/repo.git path/to/submodule

# Add a submodule with a specific branch
git submodule add -b branch-name https://github.com/username/repo.git path/to/submodule
```

### Initializing Submodules
```bash
# Initialize submodules after cloning
git submodule init

# Initialize and update submodules
git submodule update --init

# Initialize and update recursively
git submodule update --init --recursive
```

### Updating Submodules
```bash
# Update submodules to latest commit on tracked branch
git submodule update --remote

# Update specific submodule
git submodule update --remote path/to/submodule

# Update all submodules
git submodule foreach git pull origin master
```

### Cloning with Submodules
```bash
# Clone a repository with all submodules
git clone --recurse-submodules https://github.com/username/repo.git
```

## Advanced Operations

These are specialized Git commands for specific scenarios that go beyond everyday usage. They help with debugging, managing multiple working directories, annotating commits, or creating and applying patches. These tools are particularly useful for complex projects and advanced Git workflows.

### Bisect (Finding Bugs)
```bash
# Start bisect
git bisect start

# Mark current version as bad
git bisect bad

# Mark a known good commit
git bisect good commit-hash

# Git will checkout commits between good and bad
# After testing, mark each as good or bad
git bisect good  # or git bisect bad

# Reset when done
git bisect reset

# Automated bisect with a test script
git bisect start
git bisect bad
git bisect good commit-hash
git bisect run ./test-script.sh
```

### Worktree
```bash
# Add a new working tree
git worktree add ../path/to/dir branch-name

# List working trees
git worktree list

# Remove a working tree
git worktree remove ../path/to/dir

# Prune deleted working trees
git worktree prune
```

### Notes
```bash
# Add a note to a commit
git notes add -m "Note message" commit-hash

# Show notes
git notes show commit-hash

# Edit a note
git notes edit commit-hash

# Remove a note
git notes remove commit-hash

# List all notes
git notes list
```

### Patch
```bash
# Create a patch
git format-patch -1 commit-hash

# Create patches for a range of commits
git format-patch master..branch-name

# Apply a patch
git apply patch-file.patch

# Apply a patch with git-am (creates commit)
git am patch-file.patch
```

### Grep
```bash
# Search for a string in tracked files
git grep "search string"

# Show line numbers
git grep -n "search string"

# Show only filenames
git grep -l "search string"

# Search in a specific commit
git grep "search string" commit-hash
```

## Git Workflows

Git workflows are standardized approaches to using Git in team environments. They define how code flows from development to production and how team members collaborate. This section outlines popular workflows that help teams coordinate their efforts, maintain clean repositories, and deliver high-quality code.

### Feature Branch Workflow
```bash
# Create a feature branch
git checkout -b feature/new-feature

# Make changes, commit them
git add .
git commit -m "Add new feature"

# Push to remote
git push -u origin feature/new-feature

# When ready, merge to main (after code review)
git checkout main
git pull
git merge feature/new-feature
git push origin main
```

### Gitflow Workflow
```bash
# Initialize gitflow
git flow init

# Start a feature
git flow feature start feature-name

# Finish a feature
git flow feature finish feature-name

# Start a release
git flow release start 1.0.0

# Finish a release
git flow release finish 1.0.0

# Start a hotfix
git flow hotfix start hotfix-name

# Finish a hotfix
git flow hotfix finish hotfix-name
```

### Forking Workflow
```bash
# Clone your fork
git clone https://github.com/your-username/repo.git

# Add upstream remote
git remote add upstream https://github.com/original-owner/repo.git

# Keep your fork up to date
git fetch upstream
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

### Centralized Workflow
```bash
# Clone the repository
git clone https://github.com/project/repo.git

# Make changes
git add .
git commit -m "Fix bug"

# Pull with rebase to avoid merge commits
git pull --rebase origin main

# Push changes
git push origin main
```

## Git Hooks

Git hooks are scripts that automatically run before or after Git events like commits, pushes, or merges. They allow you to automate checks, enforce standards, and integrate with other tools. Hooks can prevent commits that don't meet quality standards or trigger continuous integration processes automatically.

Git hooks are scripts that run automatically when certain events occur. They are stored in the `.git/hooks` directory.

### Common Hook Types
- `pre-commit`: Runs before a commit is created
- `prepare-commit-msg`: Runs before the commit message editor is launched
- `commit-msg`: Runs after the commit message is created
- `post-commit`: Runs after a commit is created
- `pre-push`: Runs before a push operation
- `pre-rebase`: Runs before a rebase operation
- `post-checkout`: Runs after a checkout operation
- `post-merge`: Runs after a merge operation

### Example Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint

# If linting fails, stop the commit
if [ $? -ne 0 ]; then
  echo "Linting failed, commit aborted"
  exit 1
fi
```

### Making Hooks Executable
```bash
chmod +x .git/hooks/pre-commit
```

## Troubleshooting

Even experienced Git users encounter problems occasionally. This section covers common issues like merge conflicts, lost commits, or authentication problems, and provides solutions to resolve them. These troubleshooting techniques help you recover from mistakes and fix repository issues without losing work.

### Common Issues and Solutions

#### Merge Conflicts
```bash
# Abort a conflicted merge
git merge --abort

# Fix conflicts manually, then
git add .
git commit

# Use merge tool
git mergetool
```

#### Reset to a Good State
```bash
# Discard all local changes
git reset --hard HEAD

# Go back to a specific commit
git reset --hard commit-hash

# Undo a pushed commit (creates a new commit)
git revert commit-hash
```

#### Fix Detached HEAD
```bash
# Create a branch at current detached HEAD
git branch temp-branch
git checkout temp-branch

# Or in one step
git checkout -b temp-branch
```

#### Recover Lost Commits
```bash
# Find lost commits using reflog
git reflog

# Create a branch at the lost commit
git branch recovery-branch commit-hash
```

#### Fix Wrong Commit Message
```bash
# Fix the last commit message
git commit --amend -m "Correct message"

# Fix older commit messages with interactive rebase
git rebase -i HEAD~3
# Change "pick" to "reword" for commits to edit
```

#### Restore Deleted Branch
```bash
# Find the commit the branch pointed to
git reflog

# Create branch at that commit
git branch branch-name commit-hash
```

#### Performance Issues
```bash
# Create a shallow clone to reduce repository size
git clone --depth=1 repository-url

# Prune unnecessary objects
git gc --prune=now --aggressive

# Use sparse checkout for large repositories
git config core.sparseCheckout true
echo "path/to/dir/*" > .git/info/sparse-checkout
git read-tree -mu HEAD
```

#### Authentication Issues
```bash
# Store credentials
git config --global credential.helper store

# Cache credentials temporarily
git config --global credential.helper "cache --timeout=3600"
```

### Diagnosis Commands
```bash
# Show repository status
git status

# Show reference logs (history of HEAD and branches)
git reflog

# File system check of repository
git fsck

# List corrupt objects
git fsck --full

# Fix corruption and optimize repository
git gc --prune=now
```

---

## Git Best Practices

1. **Commit Messages**
   - Write descriptive commit messages
   - Use the imperative mood (e.g., "Fix bug" not "Fixed bug")
   - Keep the first line under 50 characters
   - Add detailed explanation in the body if needed

2. **Branching Strategy**
   - Keep the `main` branch always deployable
   - Use feature branches for new development
   - Delete branches after merging
   - Regularly update feature branches with changes from `main`

3. **Commit Granularity**
   - Make small, focused commits
   - Commit related changes together
   - Commit often to avoid losing work

4. **Code Reviews**
   - Use pull/merge requests for code reviews
   - Review code before merging to main branches
   - Ensure CI/CD tests pass before merging

5. **Keep History Clean**
   - Use rebase to keep history linear
   - Squash trivial commits before pushing
   - Don't force push to shared branches

6. **Tags and Releases**
   - Tag all releases with version numbers
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Create annotated tags with descriptions

7. **Backup**
   - Regularly push to remote repositories
   - Have multiple remotes for important projects
   - Use pull requests as a form of backup
