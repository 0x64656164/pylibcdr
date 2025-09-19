import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_extension
from platform import python_version
from Cython.Build import cythonize

import six
if six.PY2:
    try:
        import pathlib2 as pathlib
    except ImportError:
        raise ImportError("Please install pathlib2 to continue")
else:
    import pathlib

class CMakeExtension(Extension, object):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super(CMakeExtension, self).__init__(name, sources=[])


class build_ext(build_extension, object):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super(build_ext, self).run()

    def build_cmake(self, ext):
        root = str(pathlib.Path().absolute())
        print("Root directory: {}".format(root))
        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        ext_path = self.get_ext_fullpath(ext.name) + '_' if six.PY2 else self.get_ext_fullpath(ext.name)
        extdir = pathlib.Path(ext_path)
        extdir.mkdir(parents=True, exist_ok=True)
        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        
        # Получаем информацию о Python для правильной линковки
        import sysconfig
        python_lib_dir = sysconfig.get_config_var('LIBDIR')
        python_include_dir = sysconfig.get_config_var('INCLUDEPY')
        
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config,
            '-DPYTHON_VERSION=' + python_version(),
            '-DPYTHON_LIBRARY=' + python_lib_dir,
            '-DPYTHON_INCLUDE_DIR=' + python_include_dir,
            '-DCMAKE_POSITION_INDEPENDENT_CODE=ON',  # Важно для Termux
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--', '-j2'  # Уменьшаем для Termux
        ]
        os.chdir(str(build_temp))
        self.spawn(['cmake', os.path.join(root, 'pylibcdr')] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        # Troubleshooting: if fail on line above then delete all possible
        # temporary CMake files including "CMakeCache.txt" in top level dir.
        os.chdir(root)

# cythonize pyx file if right version of Cython is found
pyx_ext = Extension("libcdr_interface",
            sources=["pylibcdr/libcdr_interface.pyx"],
            include_dirs=["pylibcdr/core"],
            language="c++",
            extra_compile_args=["-fPIC"],  # Добавляем для Termux
            extra_link_args=["-fPIC"],     # Добавляем для Termux
            )
directives = {'language_level' : "2" if six.PY2 else "3"}
cythonize(pyx_ext, compiler_directives={'language_level' : "3"})

setup(
    name="pylibcdr",
    version="0.1.1",  # Обновляем версию
    description="A wrapper around libcdr library.",
    author="Andrey Sobolev",
    author_email="andrey.n.sobolev@gmail.com",
    url="",
    download_url="",
    packages=["pylibcdr"],
    package_dir={"pylibcdr": "pylibcdr"},
    ext_modules=[CMakeExtension("pylibcdr/libcdr_interface"),],
    cmdclass={
        'build_ext': build_ext,
    }
)
