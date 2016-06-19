# from byteplay import *
#
# from pprint import pprint
# from anki.notes import Note
#
# from common_constants import UUID_FIELD_NAME
#
#
# def update_flush():
#
#     flush_code = Code.from_code(Note.flush.func_code)
#     insert_str_template = '\ninsert or replace into notes values (?,?,?,?,?,?,?,?,?,?,?{})'
#
#     insert_str_index =  flush_code.code.index((LOAD_CONST, insert_str_template.format('')))
#     flush_code.code[insert_str_index] = (LOAD_CONST, insert_str_template.format(",?"))
#
#     load_attr_index = flush_code.code.index((LOAD_ATTR, 'data'))
#     flush_code.code.insert(load_attr_index + 1, (LOAD_FAST, 'self'))
#     flush_code.code.insert(load_attr_index + 2,  (LOAD_ATTR, UUID_FIELD_NAME))
#     flush_code.code[load_attr_index+3] = (CALL_FUNCTION, 13)
#
#     pprint(flush_code.code)
#
#     Note.flush.__func__.func_code = flush_code.to_code()
#
# update_flush()