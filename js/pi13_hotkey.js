import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const TARGET_TITLE = "pi13";
const TARGET_TYPES = new Set(["PreviewImage", "SaveImage"]);

// Evita disparar el atajo mientras se escribe en un widget de texto.
function isTyping() {
    const el = document.activeElement;
    if (!el) return false;
    return el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.isContentEditable;
}

function notify(summary, detail) {
    // El toast solo existe en frontends recientes; el log siempre queda.
    try {
        app.extensionManager?.toast?.add({ severity: "warn", summary, detail, life: 4000 });
    } catch (e) {
        // Sin toast disponible, nos quedamos con la consola.
    }
    console.warn(`[pi13] ${summary} — ${detail}`);
}

function findTargetNode() {
    const nodes = app.graph?._nodes ?? [];
    return nodes.find((n) => n.title === TARGET_TITLE && TARGET_TYPES.has(n.type)) ?? null;
}

// Fallback para cuando el nodo no expone .imgs: reconstruimos la URL desde
// app.nodeOutputs, cuyas claves pueden ser el id pelado o un locator de subgrafo.
function urlFromNodeOutputs(node) {
    const outputs = app.nodeOutputs;
    if (!outputs) return null;

    const id = String(node.id);
    const key = Object.keys(outputs).find((k) => k === id || k.endsWith(":" + id));
    const image = key && outputs[key]?.images?.[0];
    if (!image?.filename) return null;

    const params = new URLSearchParams({
        filename: image.filename,
        subfolder: image.subfolder ?? "",
        type: image.type ?? "temp",
    });
    return api.apiURL(`/view?${params}`);
}

function openFirstImage() {
    const node = findTargetNode();
    if (!node) {
        notify("Nodo no encontrado", `No hay ningun PreviewImage o SaveImage titulado "${TARGET_TITLE}".`);
        return;
    }

    const url = node.imgs?.[0]?.src ?? urlFromNodeOutputs(node);
    if (!url) {
        notify("Sin imagen", `El nodo "${TARGET_TITLE}" todavia no ha generado ninguna imagen.`);
        return;
    }

    window.open(url, "_blank", "noopener,noreferrer");
}

app.registerExtension({
    name: "ComfyUI.xStructuredPrompt.Pi13Hotkey",
    setup() {
        // Fase de captura: nos adelantamos a cualquier otro handler de teclado.
        window.addEventListener("keydown", (e) => {
            if (e.key !== "F3") return;
            if (e.ctrlKey || e.altKey || e.metaKey || e.shiftKey) return;
            if (isTyping()) return;

            // F3 es "buscar siguiente" en el navegador; lo anulamos.
            e.preventDefault();
            e.stopPropagation();

            openFirstImage();
        }, true);
    },
});
