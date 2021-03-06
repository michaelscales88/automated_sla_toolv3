import json
import logging
from logging import _loggerClass
import logging.config
from automated_sla_tool.src.StackedTracebackDecorator import StackedTracebackDecorator as tb_decorator
from automated_sla_tool.src.for_all_methods_decorator import for_all_methods_decorator as all_decorate


class SysLog(_loggerClass):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self._data = self.jsonify_indented_tree(self.create_nested_str(kwargs.get('file_path', None)))

    def create_nested_str(self, f_path):
        with open(f_path, 'r', encoding='utf-8') as file:
            nested_strings = [line.rstrip() for line in file]
        print(nested_strings)
        return nested_strings

    def get_kvl(self, line):
        key = line.split(":")[0].strip()
        value = line.split(":")[1].strip()
        level = len(line) - len(line.lstrip())
        return {'key': key, 'value': value, 'level': level}

    def pp_json(self, json_thing, sort=True, indents=4):
        if type(json_thing) is str:
            json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents)
        else:
            json.dumps(json_thing, sort_keys=sort, indent=indents)
        return None

    def jsonify_indented_tree(self, tree):  # convert shitty sgml header into json
        level_map = {0: []}
        tree_length = len(tree) - 1
        for i, line in enumerate(tree):
            data = self.get_kvl(line)
            if data['level'] not in level_map.keys():
                level_map[data['level']] = []  # initialize
            prior_level = self.get_kvl(tree[i - 1])['level']
            level_dif = data['level'] - prior_level  # +: line is deeper, -: shallower, 0:same
            if data['value']:
                level_map[data['level']].append({data['key']: data['value']})
            if not data['value'] or i == tree_length:
                if i == tree_length:  # end condition
                    level_dif = -len(list(level_map.keys()))
                if level_dif < 0:
                    for level in reversed(range(prior_level + level_dif + 1, prior_level + 1)):  # (end, start)
                        # check for duplicate keys in current deepest (child) sibling group,
                        # merge them into a list, put that list in a dict
                        key_freq = {}  # track repeated keys
                        for n, dictionary in enumerate(level_map[level]):
                            current_key = list(dictionary.keys())[0]
                            if current_key in list(key_freq.keys()):
                                key_freq[current_key][0] += 1
                                key_freq[current_key][1].append(n)
                            else:
                                key_freq[current_key] = [1, [n]]
                        for k, v in key_freq.items():
                            if v[0] > 1:  # key is repeated
                                duplicates_list = []
                                for index in reversed(v[1]):  # merge value of key-repeated dicts into list
                                    duplicates_list.append(list(level_map[level].pop(index).values())[0])
                                level_map[level].append(
                                    {k: duplicates_list})  # push that list into a dict on the same stack it came from
                        if i == tree_length and level == 0:  # end condition
                            # convert list-of-dict into dict
                            parsed_nest = {k: v for d in level_map[level] for k, v in d.items()}
                        else:
                            # push current deepest (child) sibling group onto parent key
                            key = level_map[level - 1].pop()  # string
                            # convert child list-of-dict into dict
                            level_map[level - 1].append({key: {k: v for d in level_map[level] for k, v in d.items()}})
                            level_map[level] = []  # reset deeper level
                level_map[data['level']].append(data['key'])
        return parsed_nest

    def __str__(self):
        return '\n'.join([json.dumps(self._data, sort_keys=True, indent=4)])
