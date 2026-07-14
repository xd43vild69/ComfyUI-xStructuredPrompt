import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI.xStructuredPrompt.MultilineStringSelector",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MultilineStringSelector") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Agregar el botón a la interfaz del nodo, lo llamamos solo "Add"
                const btnWidget = this.addWidget("button", "Add", "button", () => {
                    let count = 0;
                    for (let w of this.widgets) {
                        if (w.name && w.name.startsWith("string_")) {
                            count++;
                        }
                    }
                    
                    const newIndex = count + 1;
                    const newWidgetName = "string_" + newIndex;
                    
                    // Añadir la nueva caja
                    ComfyWidgets["STRING"](this, newWidgetName, ["STRING", { multiline: true }], app);
                    
                    const size = this.computeSize();
                    this.setSize([size[0], this.size[1] + 60]); 
                    this.setDirtyCanvas(true, true);
                });
                
                // Mover el botón hacia arriba.
                // this.widgets[0] es "active_index", queremos que el botón sea el segundo elemento.
                const widgetIndex = this.widgets.indexOf(btnWidget);
                if (widgetIndex > -1) {
                    this.widgets.splice(widgetIndex, 1); // Lo quitamos del final
                    this.widgets.splice(1, 0, btnWidget); // Lo insertamos en la posición 1
                }
                
                return r;
            };
        }
    }
});
