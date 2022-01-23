import os

from typing import Dict, Iterable, Set

from .editor import CodeEditor, ImportCollector
from .idl import Idl, IdlTypeDefinition, IdlTypeDefinitionTy, IdlType, EnumFields
from .utils import camel_to_snake, pascal_to_snake


class CodeGen:
    idl: Idl
    root_module: str
    source_path: str
    external_types: Dict[str, str]
    _editors: Dict[str, CodeEditor]
    _defined_types: Set[str]

    def __init__(self, idl, root_module, source_path):
        self.idl = idl
        self.root_module = root_module
        self.source_path = source_path
        self.external_types = dict()

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

    def _get_type_as_string(
        self, field_type, imports, within_types, explicit_forward_ref=False
    ):
        if field_type == IdlType.BOOL:
            return "bool"
        elif field_type <= IdlType.I128:
            imports.add_from_import("pod", field_type.get_name())
            return field_type.get_name()
        elif field_type == IdlType.BYTES:
            return "bytes"
        elif field_type == IdlType.STRING:
            return "str"
        elif field_type == IdlType.PUBLIC_KEY:
            imports.add_from_import("solana.publickey", "PublicKey")
            return "PublicKey"
        elif field_type == IdlType.DEFINED:
            self._expected_types.add(field_type.field)
            if within_types:
                imports.add_import(f"{self.root_module}.types", as_clause="types")
                if explicit_forward_ref or field_type.field in self._defined_types:
                    return f"types.{field_type.field}"
                else:
                    return f'"types.{field_type.field}"'
            else:
                imports.add_from_import(f"{self.root_module}.types", field_type.field)
                return f"{field_type.field}"
        elif field_type == IdlType.OPTION:
            imports.add_from_import(f"pod", "Option")
            if within_types:
                imports.add_import(f"{self.root_module}.types", as_clause="types")
                field_type_str = self._get_type_as_string(
                    field_type.field, imports, within_types=within_types
                )
                return f"Option[{field_type_str}]"
            else:
                imports.add_from_import(f"{self.root_module}.types", field_type.field)
                return f'"Option[{field_type.field}]"'

        elif field_type == IdlType.VEC:
            imports.add_from_import("pod", "Vec")
            elem_type = field_type.field
            elem_type_str = self._get_type_as_string(
                elem_type, imports, within_types=within_types
            )
            return f"Vec[{elem_type_str}]"

        elif field_type == IdlType.ARRAY:
            imports.add_from_import("pod", "FixedLenArray")
            elem_type, n_elem = field_type.field
            elem_type_str = self._get_type_as_string(
                elem_type, imports, within_types=within_types
            )
            return f"FixedLenArray[{elem_type_str}, {n_elem}]"

        return ""

    def _get_type_definitions(self) -> Iterable[IdlTypeDefinition]:
        return self.idl.types + self.idl.accounts

    def _generate_types(self):
        type_definitions = self._get_type_definitions()

        self._defined_types.update(self.external_types)
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
                            imports.add_from_import("typing", "Tuple")
                            variant_type = (
                                "Variant(field=Tuple[" + ", ".join(tuple_fields) + "])"
                            )

                    class_code += [f"    {variant.name.upper()}: {variant_type}\n"]
                    has_variant = True

                if not has_variant:
                    class_code += ["    pass\n"]

            editor = self._get_editor(
                f"{self.root_module}.types.{camel_to_snake(type_def.name)}"
            )

            is_clean = "imports" not in editor
            editor["imports"] = editor.wrap_with_lock(
                "imports", imports.as_source_code()
            )
            if is_clean:
                editor.add_lines("\n\n")

            class_key = f"class({type_def.name})"
            is_clean = class_key not in editor
            editor[class_key] = editor.wrap_with_lock(class_key, class_code)
            if is_clean:
                editor.add_lines(
                    "\n",
                    "    @classmethod  # type: ignore[misc]\n",
                    "    def to_bytes(cls, obj, **kwargs):\n",
                    '        return cls.pack(obj, converter="bytes", **kwargs)\n',
                    "\n",
                    "    @classmethod  # type: ignore[misc]\n",
                    "    def from_bytes(cls, raw, **kwargs):\n",
                    '        return cls.unpack(raw, converter="bytes", **kwargs)\n',
                )

            module_imports.add_from_import(
                f".{camel_to_snake(type_def.name)}", type_def.name
            )

            self._defined_types.add(type_def.name)

        editor = self._get_editor(f"{self.root_module}.types", is_file=False)
        editor[f"imports"] = editor.wrap_with_lock(
            "imports", module_imports.as_source_code()
        )

    def _generate_constants(self):
        constants = self.idl.constants
        editor = self._get_editor(f"{self.root_module}.constants")

        imports = ImportCollector()
        codes = []

        for const in constants:
            const_type = self._get_type_as_string(
                const.type, imports, within_types=False
            )
            codes.append(f"{const.name}: {const_type} = {const.value}\n")

        is_clean = "imports" not in editor
        editor["imports"] = editor.wrap_with_lock("imports", imports.as_source_code())
        if is_clean:
            editor.add_lines("\n\n")

        editor["constants"] = editor.wrap_with_lock("constants", codes)

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
        self._editors = {}
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
