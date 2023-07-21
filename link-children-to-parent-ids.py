items = [
  {'id': 1, 'parent': None, 'some_arg': 'folder'},
  {'id': 2, 'parent': 1, 'some_arg': 'folder'},
  {'id': 3, 'parent': 2, 'some_arg': 'folder'},
  {'id': 4, 'parent': 3, 'some_arg': 'file'},
  {'id': 5, 'parent': None, 'some_arg': 'folder'},
  {'id': 6, 'parent': 1, 'some_arg': 'file'},
  {'id': 7, 'parent': 2, 'some_arg': 'folder'},
]


def parent_child_structure(obj, id_key, parent_key, *args):
  """
    converts 1-2-1 id and parent id mapping to 1-2-many parent id and children ids mapping.
    i.e. groups all children ids under their parent id
    
    :param obj:
                items = [
                            {'id': 1, 'parent': None, 'some_arg': 'folder'},
                            {'id': 2, 'parent': 1, 'some_arg': 'folder'},
                            {'id': 3, 'parent': 2, 'some_arg': 'folder'},
                            {'id': 4, 'parent': 3, 'some_arg': 'file'},
                            {'id': 5, 'parent': None, 'some_arg': 'folder'},
                            {'id': 6, 'parent': 1, 'some_arg': 'file'},
                            {'id': 7, 'parent': 2, 'some_arg': 'folder'},
                        ]
    :param id_key: 'id'
    :param parent_key: 'parent'
    :param *args: 'content_type' <-- the name of any extra keys to be associated with the child
    :return map of parents mapped to list of children
        {1: [{'id': 2, 'some_arg': 'folder'}, {'id': 6, 'some_arg': 'file'}, {'id': 3, 'some_arg': 'folder'}, {'id': 7, 'some_arg': 'folder'}, {'id': 4, 'some_arg': 'file'}], 2: [{'id': 3, 'some_arg': 'folder'}, {'id': 7, 'some_arg': 'folder'}, {'id': 4, 'some_arg': 'file'}, {'id': 4, 'some_arg': 'file'}], 3: [{'id': 4, 'some_arg': 'file'}], 4: [], 5: [], 6: [], 7: []}
    """
    def crawl_relatives(relatives, families):
        if len(relatives) and len(families[relatives[0][id_key]]) and families[relatives[0][id_key]][0] != relatives[-1][id_key]:
            crawl_relatives(families[relatives[0][id_key]], families)
            relatives += families[relatives[0][id_key]]

    families = {item[id_key]: [] for item in obj}
    
    for item in obj:
        if item[parent_key] is not None:
            item_dict = {}
            if args:
                for a in args:
                    item_dict[id_key] = item[id_key]
                    item_dict[a] = item[a]
            else:
                item_dict[id_key] = item[id_key]
            
            families[item[parent_key]].append(item_dict)
            
    
    for relatives in families.values():
        crawl_relatives(relatives, families)
    
    return families

print(parent_child_structure(items, 'id', 'parent', 'content_type'))
