---
name: comfyui-node
description: Scaffold new custom ComfyUI nodes from scratch, generating the complete Python boilerplate (class with INPUT_TYPES, RETURN_TYPES, FUNCTION, CATEGORY, plus NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS) and the surrounding pack structure (__init__.py, pyproject.toml). Use this skill whenever the user wants to create, build, write, or scaffold a new ComfyUI custom node or node pack — including prompt-building/composition nodes, image/tensor nodes, or I/O utility nodes — even if they don't say the word "skill". Trigger on phrases like "make a ComfyUI node", "custom node for ComfyUI", "new node that does X", "node pack", or when they describe node behavior (inputs, outputs, a category) in a ComfyUI context.
---

# ComfyUI Custom Node Scaffolder

Generate correct, runnable ComfyUI custom nodes following the standard ComfyUI conventions. Do not impose opinionated naming, categories, or aesthetics — ask the user or use neutral defaults.

## Workflow

1. **Gather the spec.** Determine, asking only for what's missing:
   - Node display name and internal class name.
   - Inputs: name, type, and whether required/optional. Widget defaults where relevant.
   - Outputs: types and names.
   - Category (defaults to a neutral value the user picks).
   - Whether it's a single node or a pack of several.
2. **Pick the shape.** One node → single `nodes.py` + `__init__.py`. Multiple → group in `nodes.py` (or split files) and aggregate mappings in `__init__.py`.
3. **Generate.** Write the class(es) per the anatomy below, then the `__init__.py` with mappings, then `pyproject.toml` for the registry.
4. **Deliver.** Place files under a pack directory named `ComfyUI-<PackName>/` so it drops straight into `custom_nodes/`.

## Node anatomy (the required contract)

Every node is a Python class. ComfyUI discovers it via the mappings in `__init__.py`.

```python
class ExampleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
            },
            "optional": {
                "suffix": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)     # optional; defaults to lowercased types
    FUNCTION = "execute"          # method name called at runtime
    CATEGORY = "utils"            # menu path, e.g. "prompt/compose"
    # OUTPUT_NODE = True          # only for terminal nodes (savers/previews)

    def execute(self, text, strength, suffix=""):
        result = f"{text}{suffix}"
        return (result,)          # ALWAYS a tuple, even for one output
```

Hard rules:
- `INPUT_TYPES` is a `@classmethod` returning a dict with `required` (and optionally `optional`, `hidden`).
- `RETURN_TYPES` and the returned value are **tuples**. A single output needs a trailing comma.
- The `FUNCTION` string must match a real method name; its params must match the input keys exactly.
- Types are strings: `"STRING"`, `"INT"`, `"FLOAT"`, `"BOOLEAN"`, `"IMAGE"`, `"LATENT"`, `"CONDITIONING"`, `"MODEL"`, `"CLIP"`, `"VAE"`, etc. A Python list of strings makes a dropdown: `(["a", "b"], {"default": "a"})`.

See `references/types_and_widgets.md` for the full widget-option catalog and every built-in type.

## The `__init__.py` (discovery)

```python
from .nodes import ExampleNode

NODE_CLASS_MAPPINGS = {
    "ExampleNode": ExampleNode,          # unique global key
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "ExampleNode": "Example Node",       # shown in the menu
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
```

Keys in `NODE_CLASS_MAPPINGS` must be globally unique across all installed packs — prefix them if collision is likely.

## `pyproject.toml` (for the ComfyUI registry)

```toml
[project]
name = "comfyui-<packname>"
version = "1.0.0"
description = "<short description>"
requires-python = ">=3.9"
dependencies = []

[tool.comfy]
PublisherId = "<publisher>"
DisplayName = "<Pack Display Name>"
```

Only include `dependencies` the nodes actually import beyond ComfyUI's own environment (torch, numpy, PIL are already present).

## Prompt-building nodes

These are the most common request here. They almost always:
- Take one or more `STRING` inputs with `{"multiline": True}`.
- Assemble them in a defined order, optionally with weights `(text:1.2)` or separators.
- Return a single `STRING` (or `CONDITIONING` if they also encode via a `CLIP` input).

Read `references/prompt_nodes.md` before writing any prompt/composition node — it has ready patterns for ordered section builders, weighted composition, and CLIP-encoding variants.

## Common mistakes to avoid

- Returning a bare value instead of a tuple → ComfyUI errors on unpacking.
- `INPUT_TYPES` param names not matching the `FUNCTION` signature.
- Forgetting `RETURN_TYPES` is a tuple (single output missing the comma).
- Using `OUTPUT_NODE = True` on a normal node (only savers/previews need it).
- Duplicate `NODE_CLASS_MAPPINGS` keys across packs.
- For lazy re-execution control, remember `IS_CHANGED` — cover it only if the node reads external/mutable state (files, time, randomness); see the reference.
