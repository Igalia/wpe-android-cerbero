# wpe-android-cerbero

This is a fork of [GStreamer's cerbero](https://gitlab.freedesktop.org/gstreamer/cerbero).
It builds WPE WebKit and its dependencies for Android.
[wpe-android](https://github.com/Igalia/wpe-android) downloads the packages it makes.

This page only covers what the fork adds.
For how cerbero works, see the upstream [README.md](../README.md).

## Versions

| What | Where it is set |
| --- | --- |
| Upstream cerbero base (the `1.28` branch) | `CERBERO_VERSION` in `cerbero/enums.py` |
| WebKit commit | `commit` in `recipes/wpewebkit.recipe` |
| Package version | `version` in `packages/wpewebkit*.package` |
| Android NDK | `NDK_VERSION` in `cerbero/bootstrap/android.py` |
| Android API level | `target_distro_version` in `config/cross-android-*.cbc` |

CI builds for arm64 and x86_64.

## What the fork adds

- `recipes/wpewebkit.recipe`: builds WPE WebKit from a WebKit commit.
  Set `WPEWEBKIT_COMMIT` in the environment to build another commit.
- `recipes/wpeandroid.recipe`: ships the NDK's `libc++_shared.so`.
- `packages/wpewebkit.package` and `packages/wpewebkit-core.package`: the packages wpe-android uses.
- `packages/wpewebkit-deps.package` and `packages/wpewebkit-deps-core.package`: the same packages without
  WPE WebKit, to build WebKit against them.
  `wpewebkit-core` depends on `wpewebkit-deps-core`, so the dependencies are listed only once.
- Android fixes in some upstream recipes and in the Android build setup.
  They are the commits on top of the upstream `1.28` branch.

## Dependencies

WPE WebKit depends on these cerbero recipes:
icu, freetype, gettext, gstreamer-1.0, gst-plugins-base-1.0, gst-plugins-good-1.0, gst-plugins-bad-1.0,
harfbuzz, libepoxy, libgcrypt, libjpeg-turbo, libpng, libsoup, libtasn1, libxslt, libwebp, openjpeg,
openxr and xkbcommon.
The `deps` list in `recipes/wpewebkit.recipe` is the full, current list.

## Building the packages

```
./cerbero-uninstalled -c config/cross-android-arm64.cbc bootstrap
./cerbero-uninstalled -c config/cross-android-arm64.cbc package -f wpewebkit
./cerbero-uninstalled -c config/cross-android-arm64.cbc package -f wpewebkit-deps
```

This makes `wpewebkit-android-arm64-<version>.tar.xz` and `wpewebkit-android-arm64-<version>-runtime.tar.xz`,
and the same two for `wpewebkit-deps`.

## Releases

CI builds every pull request.
When a pull request is merged, CI uploads the packages to `https://wpewebkit.org/android/bootstrap/<version>/`.

To bump WebKit:

1. Change `commit` in `recipes/wpewebkit.recipe`.
2. Bump `version` in the four package files.
3. After the packages are uploaded, set `default_version` in wpe-android's `tools/scripts/bootstrap.py` to the new version.
