import pkg_resources

packages = [
    "flask", "werkzeug", "langchain_community", "langchain_core", "flask_mail","langhain",
    "flask_pymongo", "python-dotenv", "pandas", "selenium", "webdriver_manager"
]

for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"{package} version: {version}")
    except pkg_resources.DistributionNotFound:
        print(f"{package} is not installed.")
