import json
import requests
from tqdm import tqdm
import os

# Constants
JSON_URL = "https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json"
PYPI_API_URL = "https://pypi.org/pypi/{package}/json"
CACHE_FILE = "pypi_package_sizes.json"

def fetch_top_packages(json_url):
    """Fetch the JSON file containing the top PyPI packages."""
    response = requests.get(json_url)
    response.raise_for_status()
    return response.json()

def get_package_size(package_name):
    """Fetch the size of all files in the latest release for a package."""
    try:
        response = requests.get(PYPI_API_URL.format(package=package_name))
        response.raise_for_status()
        data = response.json()
        # Get the latest version
        latest_version = data["info"]["version"]
        # Get all files for the latest version
        release_files = data.get("releases", {}).get(latest_version, [])
        # Sum the size of all files in the release
        total_size = sum(file.get("size", 0) for file in release_files)
        return total_size
    except Exception as e:
        print(f"Failed to fetch size for {package_name}: {e}")
        return 0

def load_cache(cache_file):
    """Load the cached package sizes from a local JSON file."""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache_file, cache_data):
    """Save the package sizes to a local JSON file."""
    with open(cache_file, "w") as f:
        json.dump(cache_data, f, indent=2)

def estimate_total_size(packages, top_n, cache_file):
    """Estimate the total size of the top `n` packages."""
    cache = load_cache(cache_file)
    total_size_bytes = 0

    for pkg in tqdm(packages[:top_n], desc=f"Processing top {top_n} packages"):
        package_name = pkg["project"]
        if package_name in cache:
            size = cache[package_name]
        else:
            size = get_package_size(package_name)
            cache[package_name] = size
        total_size_bytes += size

    # Save updated cache
    save_cache(cache_file, cache)

    total_size_gb = total_size_bytes / (1024 ** 3)  # Convert bytes to GB
    print(f"Estimated total size of top {top_n} packages: {total_size_gb:.2f} GB")
    return total_size_gb

def main():
    # Step 1: Fetch the JSON data
    print("Fetching top PyPI packages...")
    data = fetch_top_packages(JSON_URL)
    packages = data["rows"]

    # Step 2: Ask user for the number of packages to process
    top_n = int(input("Enter the number of top packages to process (e.g., 100, 1000): "))

    # Step 3: Estimate total size
    estimate_total_size(packages, top_n, CACHE_FILE)

if __name__ == "__main__":
    main()