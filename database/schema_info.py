import os
from sqlalchemy import create_engine, inspect

DB_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce.db')

def get_engine():
    return create_engine(f'sqlite:///{DB_PATH}')

def get_schema_dict():
    engine = get_engine()
    inspector = inspect(engine)
    schema = {}
    for table in inspector.get_table_names():
        columns = []
        for col in inspector.get_columns(table):
            columns.append({
                'name': col['name'],
                'type': str(col['type']),
                'primary_key': col.get('primary_key', False)
            })
        fks = []
        for fk in inspector.get_foreign_keys(table):
            fks.append({
                'column': fk['constrained_columns'][0],
                'references': f"{fk['referred_table']}.{fk['referred_columns'][0]}"
            })
        schema[table] = {'columns': columns, 'foreign_keys': fks}
    return schema

def get_schema_string():
    schema = get_schema_dict()
    lines = []
    relationships = []

    for table, info in schema.items():
        col_parts = []
        for col in info['columns']:
            pk = ', PK' if col['primary_key'] else ''
            col_parts.append(f"{col['name']} ({col['type']}{pk})")
        lines.append(f"TABLE: {table}")
        lines.append(f"COLUMNS: {', '.join(col_parts)}")
        lines.append("")
        for fk in info['foreign_keys']:
            relationships.append(f"- {table}.{fk['column']} → {fk['references']}")

    if relationships:
        lines.append("RELATIONSHIPS:")
        lines.extend(relationships)

    return '\n'.join(lines)

def get_sample_values(table_name, column_name, limit=5):
    engine = get_engine()
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text(
            f"SELECT DISTINCT {column_name} FROM {table_name} LIMIT {limit}"
        ))
        return [row[0] for row in result.fetchall()]

if __name__ == '__main__':
    print(get_schema_string())