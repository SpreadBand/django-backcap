from distutils.core import setup


setup(
    name = "django-backcap",
    version = __import__("announcements").__version__,
    author = "Guillaume Libersat",
    author_email = "guillaume@spreadband.com",
    description = "Support module for community driven django websites.",
    long_description = open("README.rst").read(),
    license = "GPL v3",
    url = "http://github.com/SpreadBand/django-backcap",
    packages = [
        "backcap",
    ],
    include_package_data = True,
    package_data = {
        'backcap': [
            'locale/*/*/*',
        ]
    },
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
