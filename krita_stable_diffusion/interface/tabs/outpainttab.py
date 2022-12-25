from krita import *
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab


class OutpaintTab(GenerateTab):
    """
    OutpaintTab interface for text to image generation.
    """
    name = "OutpaintTab"
    display_name = "outpaint"
    config_name = "outpaint"
    do_random_seed = False
    outpaint_node = None
    max_width = 512
    max_height = 512

    def move_node(self, _val):
        if self.outpaint_node:
            x = int(self.config.value("outpaint_layer_x", 0))
            y = int(self.config.value("outpaint_layer_y", 0))
            self.outpaint_node.move(x, y)

    def move_node_to(self, x, y):
        if self.outpaint_node:
            self.outpaint_node.move(x, y)

    def create_outpaint_layer(self):
        d = Krita.instance().activeDocument()
        prev_layer = d.activeNode()

        # get layer named "outpaint" if it exists
        layer = d.nodeByName("outpaint")
        if layer is None:
            i = InfoObject()
            i.setProperty("color", "red")
            s = Selection()
            s.select(0, 0, self.max_width, self.max_height, 255)
            n = d.createFillLayer("outpaint", "color", i, s)
            r = d.rootNode()
            c = r.childNodes()
            r.addChildNode(n, c[len(c) - 1])
            n.setOpacity(25)

            # move the layer to the right
            n.setLocked(True)

            d.refreshProjection()

            self.outpaint_node = n

            x = int(self.config.value("outpaint_layer_x", 0))
            y = int(self.config.value("outpaint_layer_y", 0))
            self.move_node_to(x, y)

            if prev_layer:
                d.setActiveNode(prev_layer)

    def handle_tab_click(self, tab_index):
        if tab_index == 3:
            d = Krita.instance().activeDocument()
            if d:
                self.max_width = d.width() / 2
                self.max_height = d.height() / 2
                self.create_outpaint_layer()
        elif self.outpaint_node:
            # delete outpaint_node
            self.outpaint_node.remove()
