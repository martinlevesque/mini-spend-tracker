import re
import json


def decode_line(line, rules):
    for rule in rules:
        pattern_info = json.loads(rule['pattern'])
        pattern = pattern_info['pattern']
        variable_positions = pattern_info.get('variable_positions')

        category = rule['category']

        result_search = re.search(pattern, line)

        if not result_search:
            continue

        match = result_search.groups()

        if match:
            result = {
                'category': category
            }

            if category == 'skip':
                return result

            found_all = True

            for variable_name, position in variable_positions.items():
                if position < len(match):
                    result[variable_name] = match[position]
                else:
                    found_all = False
                    break

            if not found_all:
                # need to skip this rule
                continue

            return result

    return None
