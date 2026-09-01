from setuptools import setup, find_packages

setup(
    name="meow-lib",  # نام کتابخانه در PyPI
    version="1.0.0",
    description="کتابخانه اختصاصی ربات میویی برای روبیکا",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Meow Team",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",  # وابستگی‌های کتابخانه
    ],
    python_requires=">=3.8",
)