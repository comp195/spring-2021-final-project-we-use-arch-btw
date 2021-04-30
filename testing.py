import pkg_resources
import LVL

data = pkg_resources.resource_filename("LVL.UI", "setup.py")

print(data)