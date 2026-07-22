from .structured_prompt import StructuredPromptBuilder, MultilineStringSelector, EmptyLatentInverse

WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "StructuredPromptBuilder": StructuredPromptBuilder,
    "MultilineStringSelector": MultilineStringSelector,
    "EmptyLatentInverse": EmptyLatentInverse
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StructuredPromptBuilder": "Structured Prompt Builder",
    "MultilineStringSelector": "Multiline String Selector",
    "EmptyLatentInverse": "Empty Latent Image (Inverse)"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
