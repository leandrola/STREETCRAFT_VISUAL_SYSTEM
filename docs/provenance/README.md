# Provenance and build history

These files describe earlier builds, not a second Streetcraft client. Their content and checksum entries retain their original meaning.

- [Reconstruction narrative](RECONSTRUCTION_PROVENANCE.md)
- [Preparation manifest](PREP_MANIFEST.json) · [Preparation SHA manifest](PREP_SHA256SUMS.json)
- [Development SHA manifest](DEV_SHA256SUMS.json)
- [Integrated-build SHA manifest](INTEGRATED_SHA256SUMS.json)
- [1.9.1 patch manifest](PATCH_MANIFEST_1_9_1.json)

The checksum/manifests above were moved **byte-for-byte**. Paths inside them are rooted in their original package snapshots, not relative to this directory. Do not rewrite them to match the current tree or treat a historical hash mismatch as permission to alter evidence. The [root hygiene report](../repository/ROOT_HYGIENE_REPORT.md) records old-to-new locations; Git retains the earlier snapshot.

[RECONSTRUCTION_PROVENANCE.json](../../RECONSTRUCTION_PROVENANCE.json) remains at the repository root because the active regression runner opens that exact path. Its embedded-asset paths still point to unchanged fixtures. [PACKAGE_MANIFEST.json](../../PACKAGE_MANIFEST.json) also remains at root because it describes SVS 1.10.0 STABLE.

The [original Stable checksum manifest](../../SVS_1_10_0_SHA256SUMS.json), historical validation manifests and earlier cleanup checksums are preserved unchanged. For this reorganized tree, use the separate [post-cleanup manifest](../repository/POST_CLEANUP_TREE_SHA256SUMS.json). It excludes itself and local Git/browser/environment/cache state; it does not supersede the promotion evidence.
