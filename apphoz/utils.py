


def template_parameter(template, name, value):
    for i in range(0, len(template['spec']['template']['parameters'])):
        if template['spec']['template']['parameters'][i]['name'] == name:
            template['spec']['template']['parameters'].pop(i)
            param = {
                'name': name,
                'value': value
            }
            template['spec']['template']['parameters'].append(param)
            return True

    return False
