import nisyscfg

line_format = '{:<45} {:<25} {:<25} {:<25}'
print(line_format.format('Name', 'Model', 'Serial Number', 'Firmware Revision'), "\n")

with nisyscfg.Session() as session:
    # Print user aliases for all National Instruments devices in the local system
    filter = session.create_filter()
    filter.is_present = True
    filter.is_ni_product = True
    filter.is_device = True
    for resource in session.find_hardware(filter):
        print(line_format.format(resource.expert_user_alias[0], 
                                 resource.product_name, 
                                 resource.serial_number, 
                                 resource.firmware_revision if resource.supports_firmware_update == True else 'N/A'))