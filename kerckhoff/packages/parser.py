from collections import namedtuple
from typing import Any, List, NamedTuple


def squash_prefix(prefix: str, to_squash: str) -> str:
    def _squash_prefix(prefix: str, to_squash: str) -> str:
        if to_squash.startswith(prefix):
            return _squash_prefix(prefix, to_squash[len(prefix):])
        else:
            return prefix + to_squash

    if to_squash.startswith(prefix):
        return _squash_prefix(prefix, to_squash)
    else:
        return to_squash


class Parser(object):
    """A parser for the ArchieML language
    """

    _buffer: str
    _last_ref: Any
    _last_key: Any

    _skip: bool

    _depth: List[NamedTuple]
    _val: dict

    SomeList = namedtuple("SomeList", "id")
    ObjectList = namedtuple("ObjectList", "id first_key")
    StringList = namedtuple("StringList", "id")
    FreeformList = namedtuple("FreeformList", "id")

    Namespace = namedtuple("Namespace", "id")

    def __init__(self, *args, **kwargs):
        self._reset()
        super().__init__(*args, **kwargs)

    # Helper Functions

    def _reset(self):
        self._depth = list()
        self._buffer = ""
        self._val = dict()
        self._last_ref = None
        self._last_key = None
        self._skip = False

    def _clear_buffer(self):
        self._buffer = ""
        self._last_ref = None
        self._last_key = None

    def _get_current_ref(self):
        ref = self._val
        in_freeform = False
        for scope in self._depth:
            if in_freeform:
                ref = ref[-1]
                assert ref.get("type") == scope.id
                ref = ref.get("value")
                in_freeform = False
            else:
                levels = scope.id.split(".")
                for level in levels:
                    if isinstance(ref, list):
                        ref = ref[-1]
                    ref = ref.get(level)
                if isinstance(scope, self.FreeformList):
                    in_freeform = True
        assert ref is not None
        return ref

    def _access_or_create(self, key: str, thing):
        loc = None
        if isinstance(thing, dict):
            loc = thing.get(key)
            if loc is None or not isinstance(loc, dict):
                thing[key] = dict()
                loc = thing[key]
        elif isinstance(thing, list):
            if not len(thing):
                thing.append(dict())
            loc = thing[-1]
            loc[key] = dict()
            loc = loc[key]
        return loc

    def _set_value(self, path: List[str], value, replace=True):
        ref = self._get_current_ref()
        for nesting_key in path[:-1]:
            ref = self._access_or_create(nesting_key, ref)
        if isinstance(ref, list):
            if not len(ref):
                ref.append(dict())
            ref = ref[-1]
        if replace:
            ref[path[-1]] = value
        else:
            if not ref.get(path[-1]) or type(value) != type(ref.get(path[-1])):
                ref[path[-1]] = value
        return ref

    def _append_freeform_value(self, value, key="text"):
        ref = self._get_current_ref()
        assert isinstance(ref, list)
        ref.append(dict(type=key, value=value))
        return ref

    def _append_string_value(self, value: str):
        ref = self._get_current_ref()
        assert isinstance(ref, list)
        ref.append(value)
        return ref

    def _is_array_type(self) -> bool:
        return len(self._depth) > 0 and ("List" in type(self._depth[-1]).__name__)

    def _is_freeform_array(self) -> bool:
        return len(self._depth) > 0 and isinstance(self._depth[-1], self.FreeformList)

    # Handlers

    def _handle_list_item(self, line):
        value = line.lstrip()[1:].lstrip()
        value_whitespace = value[len(value.rstrip()):]
        value = value.rstrip()

        if self._is_array_type():
            if isinstance(self._depth[-1], self.SomeList):
                self._clear_buffer()
                old_list = self._depth.pop()
                self._depth.append(self.StringList(old_list.id))
                ref = self._append_string_value(value)
                self._last_ref = ref
                self._last_key = 0
                self._buffer += value
                self._handle_comment(value_whitespace)

            elif isinstance(self._depth[-1], self.StringList):
                self._clear_buffer()
                ref = self._append_string_value(value)
                self._last_ref = ref
                self._last_key = len(ref) - 1
                self._buffer += value
                self._handle_comment(value_whitespace)
            else:
                self._handle_comment(line)
        else:
            self._handle_comment(line)

    def _handle_pair(self, line):
        key = line.split(":")[0]
        value = ':'.join(line.split(":")[1:]).lstrip()
        key = key.strip()
        value_whitespace = value[len(value.rstrip()):]
        value = value.rstrip()
        key_layers = key.split(".")

        if len(self._depth) == 0 or isinstance(self._depth[-1], self.Namespace):
            self._clear_buffer()
            ref = self._set_value(key_layers, value)
            self._last_ref = ref
            self._last_key = key_layers[-1]
            self._buffer += value
            self._handle_comment(value_whitespace)
        else:
            list_context = self._depth[-1]
            ref = None
            if isinstance(list_context, self.SomeList):
                self._clear_buffer()
                self._depth.pop()
                self._depth.append(self.ObjectList(list_context.id, key))
                ref = self._set_value(key_layers, value)
                self._handle_comment(value_whitespace)
            elif isinstance(list_context, self.ObjectList):
                self._clear_buffer()
                if list_context.first_key == key:
                    self._get_current_ref().append(dict())
                ref = self._set_value(key_layers, value)
                self._handle_comment(value_whitespace)
            elif isinstance(list_context, self.FreeformList):
                self._clear_buffer()
                self._append_freeform_value(value, key)
                self._handle_comment(value_whitespace)
            elif isinstance(list_context, self.StringList):
                # Flush to buffer
                self._handle_comment(line)

            if isinstance(ref, dict):
                # Rule of thumb - if this ref returns a dict, this can be multiline
                self._last_ref = ref
                self._last_key = key_layers[-1]
                self._buffer += value + value_whitespace
            # raise NotImplementedError()

    def _handle_end_multiline(self):
        if self._last_ref is not None and self._last_key is not None:
            self._last_ref[self._last_key] = self._buffer.strip()
            self._clear_buffer()

    def _handle_start_block(self, line):
        key = line.split("}")[0][1:].strip()
        # squash all prefixing "."s
        key = squash_prefix(".", key)
        key_list = key.split(".")

        self._clear_buffer()

        if key_list[0] == "":
            # blocks with preceding . only works in freeform arrays
            if self._is_freeform_array():
                self._append_freeform_value(dict(), key[1:])
                self._depth.append(self.Namespace(key[1:]))
            pass
        else:
            self._depth = list()
            self._set_value(key_list, dict(), replace=False)
            self._depth.append(self.Namespace(key))

    def _handle_end_block(self):
        if not self._depth:
            pass
        else:
            self._depth.pop()

    def _handle_start_array(self, line):
        key = line.split("]")[0][1:].strip()
        is_freeform = "+" in key
        if is_freeform:
            key = key.replace("+", "", 1)

        self._clear_buffer()

        key = squash_prefix(".", key)
        key_list = key.split(".")
        if key_list[0] == "":
            proper_key = ".".join(key_list[1:])
            if len(self._depth) > 0:
                current_context = self._depth[-1]
                if isinstance(current_context, self.SomeList):
                    self._set_value(key_list[1:], list())
                    parent_list = self._depth.pop()
                    self._depth.append(self.ObjectList(parent_list.id, proper_key))
                elif isinstance(current_context, self.ObjectList):
                    if current_context.first_key == proper_key:
                        self._get_current_ref().append(dict())
                    self._set_value(key_list[1:], list())
                elif isinstance(current_context, self.FreeformList):
                    self._append_freeform_value(list(), proper_key)
                elif isinstance(current_context, self.Namespace):
                    self._set_value(key_list[1:], list())
                else:  # StringList
                    self._depth.pop()
                    self._set_value(key_list[1:], list())
                if is_freeform:
                    self._depth.append(self.FreeformList(proper_key))
                else:
                    self._depth.append(self.SomeList(proper_key))
            else:
                self._set_value(key_list[1:], list())
                if is_freeform:
                    self._depth.append(self.FreeformList(proper_key))
                else:
                    self._depth.append(self.SomeList(proper_key))
        else:
            # ends this
            self._depth = list()
            self._set_value(key_list, list())
            if is_freeform:
                self._depth.append(self.FreeformList(key))
            else:
                self._depth.append(self.SomeList(key))

    def _handle_end_array(self):
        if self._is_array_type():
            self._depth.pop()

    def _handle_skip(self):
        self._skip = True
        self._clear_buffer()

    def _handle_end_skip(self):
        self._skip = False

    def _handle_comment(self, comment):
        comment_value = ""
        if isinstance(comment, str):
            comment_value = comment

        stripped_comment_value = comment_value.strip()

        if stripped_comment_value.startswith("\\"):
            comment_value = comment_value.replace("\\", "", 1)

        if self._is_freeform_array():
            if stripped_comment_value:
                self._append_freeform_value(comment_value.strip())
        else:
            self._buffer += comment_value

    def _handle_ignore(self):
        return "Done"

    def _handle_command(self, command):
        fn = {
            "start_block": self._handle_start_block,
            "end_block": self._handle_end_block,
            "end_multiline": self._handle_end_multiline,
            "start_array": self._handle_start_array,
            "end_array": self._handle_end_array,
            "skip": self._handle_skip,
            "end_skip": self._handle_end_skip,
            "ignore": self._handle_ignore,
        }.get(command.data)
        if not fn:
            raise NotImplementedError(command.data)
        if not self._skip or command.data == "end_skip":
            return fn(command)

    def get_dict(self, document) -> dict:
        self._reset()
        specials = ['[', ']', '\\', '{', '}']
        for line in document.split("\n"):
            line += "\n"
            stripped = line.strip()
            lstripped = line.lstrip()
            if stripped.lower().startswith(":endskip"):
                self._handle_end_skip()
            elif not self._skip:
                if stripped.lower().startswith(":end"):
                    self._handle_end_multiline()
                    # self._handle_end_block()
                elif stripped.lower().startswith(":skip"):
                    self._handle_skip()
                elif stripped.lower().startswith(":ignore"):
                    self._handle_ignore()
                    break
                elif stripped and stripped.startswith("*"):
                    self._handle_list_item(line)
                elif stripped and len(line.split(":")) >= 2:
                    # Is possible key pair
                    key = line.split(":")[0]
                    if key and " " not in key.strip() and all([s not in key for s in specials]):
                        self._handle_pair(line)
                    else:
                        self._handle_comment(line)
                elif stripped and stripped[0] == '{' and '}' in stripped:
                    command = stripped.split("}")[0][1:].strip()
                    if not command:
                        self._handle_end_block()
                    elif all([s not in command for s in specials]):
                        self._handle_start_block(lstripped)
                    else:
                        self._handle_comment(lstripped)
                elif stripped and stripped[0] == '[' and ']' in stripped:
                    command = stripped.split("]")[0][1:].strip()
                    if not command:
                        self._handle_end_array()
                    elif all([s not in command for s in specials]):
                        self._handle_start_array(lstripped)
                    else:
                        self._handle_comment(line)
                else:
                    self._handle_comment(line)
        return self._val

    def parse(self, input_to_parse) -> dict:
        if isinstance(input_to_parse, str):
            return self.get_dict(input_to_parse)
        else:
            raise NotImplementedError("The parser currently only supports strings!")