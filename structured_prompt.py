class StructuredPromptBuilder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "camera_and_lens": ("STRING", {"forceInput": True}),
                "subject_and_action": ("STRING", {"forceInput": True}),
                "style_and_lighting": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "xStructuredPrompt"

    def build_prompt(self, camera_and_lens=None, subject_and_action=None, style_and_lighting=None):
        parts = []
        if camera_and_lens and isinstance(camera_and_lens, str) and camera_and_lens.strip():
            parts.append(camera_and_lens.strip())
            
        if subject_and_action and isinstance(subject_and_action, str) and subject_and_action.strip():
            parts.append(subject_and_action.strip())
            
        if style_and_lighting and isinstance(style_and_lighting, str) and style_and_lighting.strip():
            parts.append(style_and_lighting.strip())
            
        result = ", ".join(parts)
        
        return (result,)

class MultilineStringSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "active_index": ("INT", {"default": 1, "min": 1, "max": 99, "step": 1}),
                "string_1": ("STRING", {"multiline": True, "default": ""}),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_string",)
    FUNCTION = "select_string"
    CATEGORY = "xStructuredPrompt"

    def select_string(self, active_index, string_1, extra_pnginfo=None, unique_id=None, **kwargs):
        # Por defecto usamos string_1
        strings = [string_1]
        
        # En ComfyUI, los campos dinámicos de JS que no están en INPUT_TYPES
        # no se envían a kwargs. Debemos extraerlos del grafo visual guardado en extra_pnginfo.
        if extra_pnginfo and unique_id:
            nodes = extra_pnginfo.get("workflow", {}).get("nodes", [])
            for node in nodes:
                if str(node.get("id")) == str(unique_id):
                    widgets_values = node.get("widgets_values", [])
                    # Estructura del nodo:
                    # [0]: active_index
                    # [1]: botón "Add"
                    # [2]: string_1
                    # [3]: string_2, etc.
                    if len(widgets_values) > 2:
                        strings = widgets_values[2:]
                    break
        
        index = active_index - 1
        
        if index < 0 or index >= len(strings):
            return ("",)
            
        result = strings[index]
        
        if not isinstance(result, str):
            result = ""
            
        return (result,)
