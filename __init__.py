from .structured_prompt import StructuredPromptBuilder, MultilineStringSelector

NODE_CLASS_MAPPINGS = {
    "StructuredPromptBuilder": StructuredPromptBuilder,
    "MultilineStringSelector": MultilineStringSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StructuredPromptBuilder": "Structured Prompt Builder",
    "MultilineStringSelector": "Multiline String Selector"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
