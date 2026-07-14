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
                    const newLabelName = "label_" + newIndex;
                    const newWidgetName = "string_" + newIndex;
                    
                    // Añadir la etiqueta (label) y la nueva caja (string)
                    ComfyWidgets["STRING"](this, newLabelName, ["STRING", { default: "Estilo " + newIndex }], app);
                    ComfyWidgets["STRING"](this, newWidgetName, ["STRING", { multiline: true }], app);
                    
                    const size = this.computeSize();
                    // Aumentamos el tamaño tomando en cuenta ambas cajas
                    this.setSize([size[0], this.size[1] + 90]); 
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
                if (info && info.widgets_values) {
                    let currentCount = 0;
                    for (let w of this.widgets) {
                        if (w.name && w.name.startsWith("string_")) {
                            currentCount++;
                        }
                    }
                    
                    // Ahora cada estilo usa 2 widgets (label y string)
                    const expectedStrings = Math.floor((info.widgets_values.length - 2) / 2);
                    
                    while (currentCount < expectedStrings) {
                        currentCount++;
                        const newLabelName = "label_" + currentCount;
                        const newWidgetName = "string_" + currentCount;
                        
                        ComfyWidgets["STRING"](this, newLabelName, ["STRING", { default: "Estilo " + currentCount }], app);
                        ComfyWidgets["STRING"](this, newWidgetName, ["STRING", { multiline: true }], app);
                    }
                    
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
