import nisyscfg

line_format = '{:<105} {:<25}'
print(line_format.format('Software', 'Version'), "\n")

session = nisyscfg.Session()

for software in session.get_installed_software_components(item_types=nisyscfg.enums.IncludeComponentTypes.ALL_VISIBLE):
    print(line_format.format(software.title, software.version))

session.close()