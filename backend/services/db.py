def dict_factory(cursor, row):
    """Converts database row objects to dictionaries."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d