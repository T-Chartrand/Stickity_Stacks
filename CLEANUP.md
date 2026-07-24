Cleanup note

I created this file while cleaning up the fix/build-workflow branch.

What I changed now:
- Added .gitignore to prevent re-adding packaging/build outputs, embedded git internals, and other build artifacts.

Backup:
- A backup of the original branch was created: fix/build-workflow-backup-20260723-0000
  https://github.com/T-Chartrand/Stickity_Stacks/tree/fix%2Fbuild-workflow-backup-20260723-0000

Next steps (I recommend one of these):
1) Local rewrite (recommended, preserves a clean history):
   - Clone repo locally, checkout fix/build-workflow
   - Run the removal and history rewrite steps I outlined earlier (git rm --cached ...; git commit; git rebase origin/master; git push --force-with-lease)

2) If you want me to perform the full removal and history rewrite on the remote branch, I need permission to run lower-level git tree operations that delete files from the branch history. Those operations are destructive (force-push) but reversible using the backup branch above. Reply to confirm and I will proceed.

If you want to proceed yourself, run the commands in the PR comment or paste any conflicts here and I will guide you through resolving them.
