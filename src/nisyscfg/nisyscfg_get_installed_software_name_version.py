"""NI System Cofniguration - Get Installed Software Name and Version.
"""
import nisyscfg


line_format = "{:<105} {:<25}"
print(line_format.format("Software", "Version"), "\n")

session = nisyscfg.Session()

for software in session.get_installed_software_components():
    print(line_format.format(software.title, software.version))

session.close()
