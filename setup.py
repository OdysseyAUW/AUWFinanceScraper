from setuptools import setup, find_packages

setup(
    name='AUWFinanceScraper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas==2.1.4',
        'yfinance==0.2.35',
        'pydantic==2.5.3',
        'tqdm==4.66.1',
        'python-dotenv==1.0.0',
        'pyarrow==14.0.2',
    ],
)