#!/usr/bin/python3
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
	name='Gpyts',
	version='1.0.3',
	description='Gpyts is a library for Google translation and gTTS using Google Translation API.',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://github.com/Ripeey/Gpyts',
	license='MIT',
	author='Ripe',
	author_email='ripeey@protonmail.com',
	install_requires=[
		'aiofiles', 
		'aiohttp', 
		'requests'
	],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
	zip_safe=False,
	package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
