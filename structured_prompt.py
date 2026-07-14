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
        # Recolectamos las partes validando que no sean None ni estén vacías
        parts = []
        if camera_and_lens and isinstance(camera_and_lens, str) and camera_and_lens.strip():
            parts.append(camera_and_lens.strip())
            
        if subject_and_action and isinstance(subject_and_action, str) and subject_and_action.strip():
            parts.append(subject_and_action.strip())
            
        if style_and_lighting and isinstance(style_and_lighting, str) and style_and_lighting.strip():
            parts.append(style_and_lighting.strip())
            
        # Unimos usando coma y espacio
        result = ", ".join(parts)
        
        return (result,)

class MultilineStringSelector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "active_index": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
                "string_1": ("STRING", {"multiline": True, "default": ""}),
                "string_2": ("STRING", {"multiline": True, "default": ""}),
                "string_3": ("STRING", {"multiline": True, "default": ""}),
                "string_4": ("STRING", {"multiline": True, "default": ""}),
                "string_5": ("STRING", {"multiline": True, "default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_string",)
    FUNCTION = "select_string"
    CATEGORY = "xStructuredPrompt"

    def select_string(self, active_index, string_1, string_2, string_3, string_4, string_5):
        # Agrupamos los strings en una lista
        strings = [string_1, string_2, string_3, string_4, string_5]
        
        # Ajustamos el índice (el usuario ve de 1 a 5, en Python es de 0 a 4)
        # Nos aseguramos de que el índice no se salga de los límites
        index = max(0, min(4, active_index - 1))
        
        # Seleccionamos el string activo
        result = strings[index]
        
        # Si por alguna razón no es un string válido, devolvemos vacío
        if not isinstance(result, str):
            result = ""
            
        return (result,)
