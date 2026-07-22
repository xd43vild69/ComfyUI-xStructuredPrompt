import torch
import comfy.model_management

try:
    from nodes import MAX_RESOLUTION
except ImportError:
    MAX_RESOLUTION = 16384

# Canales del latente segun la familia de modelos.
LATENT_CHANNELS = {
    "SD1.5 / SDXL (4ch)": 4,
    "SD3 / Flux (16ch)": 16,
}


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
                "label_1": ("STRING", {"default": "Estilo 1"}),
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

    def select_string(self, active_index, label_1, string_1, extra_pnginfo=None, unique_id=None, **kwargs):
        # Por defecto usamos string_1
        strings = [string_1]
        
        # En ComfyUI, los campos dinámicos de JS que no están en INPUT_TYPES
        # no se envían a kwargs. Debemos extraerlos del grafo visual guardado en extra_pnginfo.
        if extra_pnginfo and unique_id:
            nodes = extra_pnginfo.get("workflow", {}).get("nodes", [])
            for node in nodes:
                if str(node.get("id")) == str(unique_id):
                    widgets_values = node.get("widgets_values", [])
                    # Estructura del nodo ahora:
                    # [0]: active_index
                    # [1]: botón "Add"
                    # [2]: label_1
                    # [3]: string_1
                    # [4]: label_2
                    # [5]: string_2, etc.
                    if len(widgets_values) > 2:
                        all_dynamic = widgets_values[2:]
                        # Los strings multilínea están en las posiciones impares de all_dynamic (índices 1, 3, 5...)
                        strings = all_dynamic[1::2]
                    break
        
        index = active_index - 1
        
        if index < 0 or index >= len(strings):
            return ("",)
            
        result = strings[index]
        
        if not isinstance(result, str):
            result = ""

        return (result,)

class EmptyLatentInverse:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "Ancho en pixeles. Con modelos de 16ch conviene usar multiplos de 16."}),
                "height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "Alto en pixeles. Con modelos de 16ch conviene usar multiplos de 16."}),
                "inverse": ("BOOLEAN", {"default": False, "label_on": "invertido", "label_off": "normal", "tooltip": "Intercambia width y height para probar el formato contrario sin reescribir los valores."}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096, "tooltip": "Cantidad de latentes en el lote."}),
                "model_type": (list(LATENT_CHANNELS.keys()), {"default": "SD1.5 / SDXL (4ch)", "tooltip": "Define los canales del latente. SD1.5 y SDXL usan 4; SD3 y Flux usan 16."}),
            }
        }

    RETURN_TYPES = ("LATENT", "INT", "INT")
    RETURN_NAMES = ("latent", "width", "height")
    OUTPUT_TOOLTIPS = ("El lote de latentes vacios.", "Ancho efectivo tras aplicar inverse.", "Alto efectivo tras aplicar inverse.")
    FUNCTION = "generate"
    CATEGORY = "xStructuredPrompt/utils"
    DESCRIPTION = "Crea un lote de latentes vacios con un toggle 'inverse' que intercambia ancho y alto, para alternar entre formato horizontal y vertical sin reescribir los valores."

    def generate(self, width, height, inverse, batch_size, model_type):
        if inverse:
            width, height = height, width

        channels = LATENT_CHANNELS[model_type]

        latent = torch.zeros(
            [batch_size, channels, height // 8, width // 8],
            device=comfy.model_management.intermediate_device(),
            dtype=comfy.model_management.intermediate_dtype(),
        )

        return ({"samples": latent, "downscale_ratio_spacial": 8}, width, height)
