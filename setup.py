from setuptools import setup, find_packages

setup(
    name="azure-k8s-telemetry-worker",
    version="1.0.0",
    description="Azure Kubernetes Infrastructure Telemetry Worker Service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Azure Infrastructure Team",
    packages=find_packages(),
    install_requires=[
        "newrelic>=10.12.0",
        "psutil>=7.0.0",
        "python-dotenv>=1.1.0",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "telemetry-worker=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
)
