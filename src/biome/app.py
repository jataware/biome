
from beaker_kernel.lib.app import BeakerApp


class BiomeApp(BeakerApp):
    slug = "biome"
    name = "Biome"

    pages = {
        "notebook": {
            "title": "Biome notebook",
            "default": True,
        },
        'chat': {
            "title": "Biome chat",
        },
        "dev": {
            "title": "Dev interface",
        },
        "integrations": {
            "title": "Integrations Manager"
        }
    }
    default_context = {
        "slug": "biome",
        "payload": {},
        "single_context": True,
    }

    assets = {
        "header_logo": {
            "src": "biome-logo.png",
            "alt": "Biome logo"
        },
        "body_logo": {
            "src": "biome-helix-horizontal.png",
            "alt": "Biome logo"
        }
    }

    template_bundle = {
        "short_title": "",
        "chat_welcome_html": """<div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
          <img src="{asset:body_logo:src}" alt="Biome Logo" height="100px">
          <p>Hi! I'm your Biome Agent and I can help you do all sorts of tasks related to biomedical research. I'm
          particularly good at helping with information retrieval, data analysis, and data visualization. I have
          access to a wide range of data sources and APIs including GDC, cBioPortal, and more.</p>
        </div>"""
    }
