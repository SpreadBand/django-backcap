from setuptools import setup, find_packages

setup(
    name = "django-backcap",
    author = "Guillaume Libersat",
    author_email = "guillaume@spreadband.com",
    description = "Support module for community driven django websites.",
    long_description = open("README.rst").read(),
    license = "GPL v3",
    url = "http://github.com/SpreadBand/django-backcap",
    packages = [
        "backcap",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django-notification==1.0",
                      "django-voting==0.2",
                     ],
    zip_safe=False,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
