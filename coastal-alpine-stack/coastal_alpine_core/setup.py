from setuptools import setup, find_packages

setup(
 name="coastal-alpine-core",
 version="1.2.0",
 description="Shared utilities for Coastal Alpine Tech edge agentic AI stack",
 author="Wayne Roberts, Coastal Alpine Tech",
 packages=find_packages(),
 install_requires=["requests", "ollama"],
 python_requires=">=3.10",
 classifiers=[
 "Programming Language :: Python :: 3.10",
 "License :: Other/Proprietary License",
 "Operating System :: OS Independent",
 ],
)
