def resolve_all_characters(query, info):
    return list(query.objects.all())

def resolve_query(query, info, name):
    return query.objects.get(name=name)
