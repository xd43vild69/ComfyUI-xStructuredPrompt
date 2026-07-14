import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI.xStructuredPrompt.MultilineStringSelector",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MultilineStringSelector") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                const btnWidget = this.addWidget("button", "Add", "button", () => {
                    let count = 0;
                    for (let w of this.widgets) {
                        if (w.name && w.name.startsWith("string_")) {
                            count++;
                        }
                    }
                    
                    const newIndex = count + 1;
                    const newWidgetName = "string_" + newIndex;
                    
                    ComfyWidgets["STRING"](this, newWidgetName, ["STRING", { multiline: true }], app);
                    
                    const size = this.computeSize();
                    this.setSize([size[0], this.size[1] + 60]); 
                    this.setDirtyCanvas(true, true);
                });
                
                const widgetIndex = this.widgets.indexOf(btnWidget);
                if (widgetIndex > -1) {
                    this.widgets.splice(widgetIndex, 1);
                    this.widgets.splice(1, 0, btnWidget);
                }
                
                return r;
            };

            const onConfigure = nodeType.prototype.onConfigure;
            
            nodeType.prototype.onConfigure = function (info) {
                // LiteGraph internamente intenta asignar los valores antes de llamar a onConfigure
                // Como las cajas dinámicas aún no existían, ignoró sus textos.
                
                if (info && info.widgets_values) {
                    let currentCount = 0;
                    for (let w of this.widgets) {
                        if (w.name && w.name.startsWith("string_")) {
                            currentCount++;
                        }
                    }
                    
                    const expectedStrings = info.widgets_values.length - 2;
                    
                    // 1. Recrear las cajas faltantes
                    while (currentCount < expectedStrings) {
                        currentCount++;
                        const newWidgetName = "string_" + currentCount;
                        ComfyWidgets["STRING"](this, newWidgetName, ["STRING", { multiline: true }], app);
                    }
                    
                    // 2. Forzar la asignación manual de los valores guardados a TODOS los widgets ahora que existen
                    for (let i = 0; i < this.widgets.length; i++) {
                        if (this.widgets[i] && info.widgets_values[i] !== undefined) {
                            this.widgets[i].value = info.widgets_values[i];
                        }
                    }
                }
                
                if (onConfigure) {
                    return onConfigure.apply(this, arguments);
                }
            };
        }
    }
});
