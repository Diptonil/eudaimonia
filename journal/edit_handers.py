from wagtail.admin.edit_handlers import MultiFieldPanel


class ZenModeMultiFieldPanel(MultiFieldPanel):

    template = "journal/edit_handlers/zen.html"

    def classes(self):
        classes = super().classes()
        classes.append("zen-mode-panel")
        return classes
