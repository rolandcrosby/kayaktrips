from setuptools import setup

setup(
    name="kayaktrips",
    version="1.0.0",
    description="Get your historical flight data out of Kayak Trips",
    author="Roland Crosby",
    author_email="roland@rolandcrosby.com",
    url="https://github.com/rolandcrosby/kayaktrips",
    packages=["kayaktrips"],
    install_requires=["requests", "icalendar"]
)
