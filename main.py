from typing import List, Set

from graphql import *

schemaOne = build_schema("""
    type One {
        id: Int!
        lst: [String]!
    }

    type Two {
        id: Int!
        data: String
    }

    type Three {
        id: Int!
        lst: [String]!
    }
""")

schemaTwo = build_schema("""
    type One {
        id: Int!
        lst: [String!]!
    }
    
    type Two {
        id: ID
        data2: String!
    }
    
    type Four {
        id: ID!
        lst: [String]!
    }
""")

primitive_types = {'String', 'Int', 'Float', 'Boolean', 'ID'}
internal_types = {'__Schema', '__Type', '__TypeKind', '__Field', '__InputValue', '__EnumValue', '__Directive',
                  '__DirectiveLocation'}


class Schema:
    def __init__(self, schema: GraphQLSchema):
        self.types = []
        self.columns = {}
        self.column_types = {}

        for field in schema.type_map:
            if field not in primitive_types and field not in internal_types:
                self.types.append(field)

                columns = []
                column_types = []

                for column in schema.type_map.get(field).__dict__.get('fields').items():
                    columns.append(column[0])
                    column_types.append(column[1])

                self.columns[field] = columns
                self.column_types[field] = column_types


class SchemaDiff:
    def __init__(self, old_schema: Schema, new_schema: Schema):
        self.new_types = get_new_elements(old_schema.types, new_schema.types)
        self.removed_types = get_removed_elements(old_schema.types, new_schema.types)
        self.common_types = get_common_elements(old_schema.types, new_schema.types)

        self.new_columns = []
        self.removed_columns = []
        self.changed_columns = []

        for common_type in self.common_types:
            new_columns = get_new_elements(old_schema.columns.get(common_type), new_schema.columns.get(common_type))
            removed_columns = get_removed_elements(old_schema.columns.get(common_type), new_schema.columns.get(common_type))

            for column in new_columns:
                self.new_columns.append(common_type + '.' + column)

            for column in removed_columns:
                self.removed_columns.append(common_type + '.' + column)

            if len(new_columns) == 0 and len(removed_columns) == 0:
                for i in range(len(old_schema.columns.get(common_type))):
                    if(old_schema.column_types.get(common_type).__getitem__(i).__str__() != new_schema.column_types.get(common_type).__getitem__(i).__str__()):
                        self.changed_columns.append(common_type + '.' + old_schema.columns.get(common_type).__getitem__(i))


def get_new_elements(old: List[str], new: List[str]) -> Set[str]:
    return set(new) - set(old)


def get_removed_elements(old: List[str], new: List[str]) -> Set[str]:
    return set(old) - set(new)


def get_common_elements(old: List[str], new: List[str]) -> Set[str]:
    return set(new) & set(old)


def schema_diff(schema1: GraphQLSchema, schema2: GraphQLSchema):
    old_schema = Schema(schema1)
    new_schema = Schema(schema2)
    diff = SchemaDiff(old_schema, new_schema)

    print('New types: ' + str(diff.new_types))
    print('Removed types: ' + str(diff.removed_types))
    print('New columns: ' + str(diff.new_columns))
    print('Removed columns: ' + str(diff.removed_columns))
    print('Changed columns: ' + str(diff.changed_columns))


if __name__ == '__main__':
    schema_diff(schemaOne, schemaTwo)
