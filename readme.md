# pypi-size

Get the size of the most popular pip repositories

## Usecase

Want to self host pypi repositories? How much storage to you need?
This retrieves the size of the most popular ones from: [https://hugovk.github.io/top-pypi-packages](https://github.com/hugovk/top-pypi-packages)

## Usage

````
pip install -r requirements.txt
python3 size.py
````

- Enter the number of repositories to calculate size of
- The size of the repositories will be retrieved from pypi.org
- Delete pypi_package_sizes.json to redownload information

## Results
- Top 100: 5.56 GB
- Top 1000: 46.98 GB
- Top 10000: 202.97 GB
