from setuptools import setup

setup(
    name = "weloopai",
    version = "0.0.1",
    author = "Yannick Le Cacheux",
    description = "Test for Weloop.ai",
    url = "https://github.com/yannick-lc/test-weloop",
    packages = ["weloopai"],
    package_dir={"": "src"},
    entry_points={"console_scripts": ["weloopai=weloopai.main:main"]}
)
