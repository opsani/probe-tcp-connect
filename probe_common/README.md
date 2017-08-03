# probe-common
This repository includes common code for Skopos probes.  It is included as a subtree in each of the parent probe repositories.

A subtree includes the contents of one repo as a sub-directory within another.  These contents are included in the parent with a merge commit which records the commit ID (SHA-1) of the injected sub-repo.  The git subtree script maintains a subtree-specific branch that gets merged on every `git subtree pull` and `git subtree merge`.

Using subtrees, a clone of the parent repo naturally includes the sub-repo contents (as present at the time of the merge commit).  References:

* <https://www.atlassian.com/blog/git/alternatives-to-git-submodule-git-subtree>
* <https://medium.com/\@porteneuve/mastering-git-subtrees-943d29a798ec>
* <https://stackoverflow.com/questions/32407634/when-to-use-git-subtree>

When creating a new probe, the probe-common repo contents may be included as a subtree of the new probe parent with the following commands:

* `git remote add --fetch probe_common https://github.com/opsani/probe-common`
* `git subtree add --prefix probe_common --squash probe_common master`

To update the probe-common subtree of a cloned parent repo where the subtree's remote has changed:

* As required, add the remote:  `git remote add --fetch probe_common https://github.com/opsani/probe-common`
* `git fetch probe_common master`
* `git subtree pull --prefix probe_common --squash probe_common master`

This change may be committed to update the parent repo (to include the updated contents of the subtree).
