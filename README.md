# schemaDiff

Create a SchemaDiff object using the schema_diff function.

diff = schema_diff(old_schema, new_schema)

The object has the following fields:

New types: diff.new_types  
Removed types: diff.removed_types  
New columns: diff.new_columns  
Removed columns: diff.removed_columns  
Changed columns: diff.changed_columns
