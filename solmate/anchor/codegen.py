import os

from typing import Dict, Iterable, Set, Union

from solana.publickey import PublicKey
from solana.system_program import SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID

from .editor import CodeEditor
from .idl import (
    Idl,
    IdlTypeDefinition,
    IdlTypeDefinitionTy,
    IdlType,
    EnumFields,
    IdlAccountItem,
)
from .utils import camel_to_snake, pascal_to_snake


class CodeGen:
    idl: Idl
    root_module: str
    source_path: str
    external_types: Dict[str, str]
    default_accounts: Dict[str, Union[str, PublicKey]]
    _editors: Dict[str, CodeEditor]
    _defined_types: Set[str]
    _expected_types: Set[str]

    def __init__(
        self,
        idl,
        root_module,
        source_path,
        external_types=None,
        default_accounts=None,
    ):
        self.idl = idl
        self.root_module = root_module
        self.source_path = source_path

        if external_types is None:
            self.external_types = dict()
        else:
            self.external_types = external_types

        if default_accounts is None:
            self.default_accounts = dict()
        else:
            self.default_accounts = default_accounts

        self._editors = {}
        self._defined_types = set()
        self._expected_types = set()

    def _get_editor(self, name, is_file=True) -> CodeEditor:
        if name not in self._editors:
            subpath = name.replace(".", "/")
            if not is_file:
                subpath += "/__init__"
            subpath += ".py"

            fullpath = os.path.join(self.source_path, subpath)
            self._editors[name] = CodeEditor(fullpath)
            self._editors[name].load()

        return self._editors[name]

    @staticmethod
    def _add_packing_methods(editor):
        # this allows IDE's to give better autocomplete for these methods
        # (otherwise, there is no need to add these.)
        editor.add_lines(
            "\n",
            "    @classmethod\n",
            "    def to_bytes(cls, obj, **kwargs):\n",
            '        return cls.pack(obj, converter="bytes", **kwargs)\n',
            "\n",
            "    @classmethod\n",
            "    def from_bytes(cls, raw, **kwargs):\n",
            '        return cls.unpack(raw, converter="bytes", **kwargs)\n',
        )

    def _get_type_as_string(
        self, field_type, editor, within_types, explicit_forward_ref=False
    ):
        if field_type == IdlType.BOOL:
            return "bool"
        elif field_type <= IdlType.I128:
            editor.add_from_import("pod", field_type.get_name())
            return field_type.get_name()
        elif field_type == IdlType.BYTES:
            return "bytes"
        elif field_type == IdlType.STRING:
            return "str"
        elif field_type == IdlType.PUBLIC_KEY:
            editor.add_from_import("solana.publickey", "PublicKey")
            return "PublicKey"
        elif field_type == IdlType.DEFINED:
            self._expected_types.add(field_type.field)
            if within_types:
                editor.add_import(f"{self.root_module}.types", as_clause="types")
                if explicit_forward_ref or field_type.field in self._defined_types:
                    return f"types.{field_type.field}"
                else:
                    return f'"types.{field_type.field}"'
            else:
                editor.add_from_import(f"{self.root_module}.types", field_type.field)
                return f"{field_type.field}"
        elif field_type == IdlType.OPTION:
            editor.add_from_import(f"pod", "Option")
            if within_types:
                editor.add_import(f"{self.root_module}.types", as_clause="types")
                field_type_str = self._get_type_as_string(
                    field_type.field, editor, within_types=within_types
                )
                return f"Option[{field_type_str}]"
            else:
                editor.add_from_import(f"{self.root_module}.types", field_type.field)
                return f'"Option[{field_type.field}]"'

        elif field_type == IdlType.VEC:
            editor.add_from_import("pod", "Vec")
            elem_type = field_type.field
            elem_type_str = self._get_type_as_string(
                elem_type, editor, within_types=within_types
            )
            return f"Vec[{elem_type_str}]"

        elif field_type == IdlType.ARRAY:
            editor.add_from_import("pod", "FixedLenArray")
            elem_type, n_elem = field_type.field
            elem_type_str = self._get_type_as_string(
                elem_type, editor, within_types=within_types
            )
            return f"FixedLenArray[{elem_type_str}, {n_elem}]"

        return ""

    def _get_type_definitions(self) -> Iterable[IdlTypeDefinition]:
        return self.idl.types + self.idl.accounts

    def _generate_types(self):
        type_definitions = self._get_type_definitions()
        if not type_definitions:
            return

        module_editor = self._get_editor(f"{self.root_module}.types", is_file=False)
        for type_def in type_definitions:
            editor = self._get_editor(
                f"{self.root_module}.types.{camel_to_snake(type_def.name)}"
            )
            editor.add_from_import("pod", "pod")

            class_code = ["@pod\n"]
            if type_def.type == IdlTypeDefinitionTy.STRUCT:
                class_code += [f"class {type_def.name}:\n"]
                has_field = False
                for field in type_def.type.field.fields:
                    field_name = camel_to_snake(field.name)
                    field_type = self._get_type_as_string(
                        field.type, editor, within_types=True
                    )
                    class_code.append(f"    {field_name}: {field_type}\n")
                    has_field = True

                if not has_field:
                    class_code += ["    pass\n"]

            else:
                editor.add_from_import("pod", "Enum")
                class_code += [f"class {type_def.name}(Enum):\n"]
                variants = type_def.type.field.variants
                for variant in variants:
                    if variant.fields is None:
                        variant_type = "None"
                    elif variant.fields == EnumFields.NAMED:
                        editor.add_from_import("pod", "Variant")
                        editor.add_from_import("pod", "named_fields")
                        # TODO complete me
                        named_fields = variant.fields.field
                        raise NotImplementedError()
                    else:
                        editor.add_from_import("pod", "Variant")

                        tuple_fields = []
                        for field_type in variant.fields.field:
                            tuple_fields.append(
                                self._get_type_as_string(
                                    field_type,
                                    editor,
                                    within_types=True,
                                    explicit_forward_ref=True,
                                )
                            )

                        if len(tuple_fields) == 0:
                            variant_type = "None"
                        elif len(tuple_fields) == 1:
                            variant_type = "Variant(field=" + tuple_fields[0] + ")"
                        else:
                            editor.add_from_import("typing", "Tuple")
                            variant_type = (
                                "Variant(field=Tuple[" + ", ".join(tuple_fields) + "])"
                            )

                    variant_name = pascal_to_snake(variant.name).upper()
                    class_code += [f"    {variant_name} = {variant_type}\n"]

                if not variants:
                    class_code += ["    pass\n"]

            if editor.set_with_lock(f"class({type_def.name})", class_code):
                self._add_packing_methods(editor)

            module_editor.add_from_import(
                f".{camel_to_snake(type_def.name)}", type_def.name
            )

            self._defined_types.add(type_def.name)

    def _generate_constants(self):
        if not self.idl.constants:
            return

        editor = self._get_editor(f"{self.root_module}.constants")
        code = []

        for const in self.idl.constants:
            const_type = self._get_type_as_string(
                const.type, editor, within_types=False
            )
            code.append(f"{const.name}: {const_type} = {const.value}\n")

        editor.set_with_lock("constants", code)

    def _generate_accounts(self):
        return {}

    def _generate_instructions(self):
        return {}

    def _generate_events(self):
        return {}

    def _generate_errors(self):
        return {}

    def _generate_state(self):
        if self.idl.state:
            raise NotImplementedError()

        return {}

    def generate_code(self, check_missing_types=False):
        self._generate_types()
        self._generate_constants()
        self._generate_accounts()
        self._generate_instructions()
        self._generate_events()
        self._generate_errors()
        self._generate_state()

        if check_missing_types:
            undefined_types = self._expected_types.difference(self._defined_types)
            if undefined_types:
                raise RuntimeError(
                    f"The following types are used but not defined: {undefined_types}"
                )

    def save_modules(self):
        for editor in self._editors.values():
            editor.save()


def cli():
    pass
