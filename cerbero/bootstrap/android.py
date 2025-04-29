# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import shutil

from cerbero.bootstrap import BootstrapperBase
from cerbero.bootstrap.bootstrapper import register_toolchain_bootstrapper
from cerbero.config import Distro

NDK_VERSION = 'r27c'
NDK_BASE_URL = 'https://dl.google.com/android/repository/android-ndk-%s-%s.zip'
NDK_CHECKSUMS = {
    f'android-ndk-{NDK_VERSION}-linux.zip': '59c2f6dc96743b5daf5d1626684640b20a6bd2b1d85b13156b90333741bad5cc',
    # doesn't ship as a zip file anymore
    f'android-ndk-{NDK_VERSION}-darwin.dmg': '7ec95a80d91cda7b4b69401d5c4a4c285fed729811fdf7ceba5739bc9d81e36b',
    f'android-ndk-{NDK_VERSION}-windows.zip': '27e49f11e0cee5800983d8af8f4acd5bf09987aa6f790d4439dda9f3643d2494',
}


class AndroidBootstrapper(BootstrapperBase):
    def __init__(self, config, offline, assume_yes):
        super().__init__(config, offline, 'android')
        self.prefix = self.config.toolchain_prefix
        url = NDK_BASE_URL % (NDK_VERSION, self.config.platform)
        self.fetch_urls.append((url, None, NDK_CHECKSUMS[os.path.basename(url)]))
        self.extract_steps.append((url, True, self.prefix))

    async def start(self, jobs=0):
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)
        ndkdir = os.path.join(self.prefix, 'android-ndk-' + NDK_VERSION)
        if not os.path.isdir(ndkdir):
            return
        # Android NDK extracts to android-ndk-$NDK_VERSION, so move its
        # contents to self.prefix
        for d in os.listdir(ndkdir):
            dest = os.path.join(self.prefix, d)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(os.path.join(ndkdir, d), self.prefix)
        os.rmdir(ndkdir)


def register_all():
    register_toolchain_bootstrapper(Distro.ANDROID, AndroidBootstrapper)
