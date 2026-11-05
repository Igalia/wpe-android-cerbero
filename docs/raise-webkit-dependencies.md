# Raising the dependencies of WebKit's Android build

WebKit's `Tools/Scripts/build-webkit --android`, which a build.webkit.org bot runs, builds WPE WebKit
against the `wpewebkit-deps` packages of this repository, with the same Android NDK.
WebKit pins them by file name and SHA-256 checksum in `Tools/Scripts/webkitpy/android_dependencies.py`,
and `Tools/Scripts/update-webkit-android-libs` downloads them from there.

Update those pins when WebKit needs a new dependency or a newer version of one, or when the packages
move to another NDK:

1. Change the recipes here, and the NDK in `cerbero/bootstrap/android.py` if that changes,
   then bump `version` in the four package files (see "Releases" in the [README](../.github/README.md)).
2. CI uploads the packages to `https://wpewebkit.org/android/bootstrap/<version>/`. For arm64 and
   for x86_64 they are `wpewebkit-deps-android-<arch>-<version>-<date><revision>.tar.xz` and
   `wpewebkit-deps-android-<arch>-<version>-runtime-<date><revision>.tar.xz`, and the upload step
   prints each name as "Remote filename".
3. In WebKit, set those four names and the SHA-256 checksums of the files in `DEPENDENCIES_DOWNLOADS`.
   For another NDK, also set `NDK_REVISION` and `NDK_DOWNLOAD`.
4. Build with `Tools/Scripts/build-webkit --android --release`, and with `--architecture=x86_64`,
   then upload the WebKit change for review.

Pin the names with a date, not the names without one: each upload points those to the newest files.

## Never delete dated `wpewebkit-deps` files

WebKit downloads the packages by their dated names, also when a bot or a bisection builds an older
revision of WebKit. Deleting one of those files breaks the Android build of every WebKit revision
that pins it.
