import json
import os

from beaker_kernel.lib.app import BeakerApp, BeakerAppAsset, AppConfigStrings, Context


class BiomeApp(BeakerApp):
    SLUG = "biome"
    ASSET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))

    pages = {
        'chat': {
            "title": "Biome chat",
            "default": True,
        },
        "notebook": {
            "title": "Biome notebook",
        },
        "dev": {
            "title": "Dev interface",
        }
    }
    default_context = Context(
        slug="biome",
        payload={},
    )
    single_context = True

    assets = [
        BeakerAppAsset(
            slug="header_logo",
            src="biome-logo.png",
            alt="Biome logo"
        ),
        BeakerAppAsset(
            slug="body_logo",
            src="biome-helix-horizontal.png",
            alt="Biome logo"
        )
    ]
    strings = AppConfigStrings(
        short_title="~",
        chat_welcome_html="""<div style="display: flex; flex-direction: row; align-items: center; gap: 20px;">
          <img src="/assets/biome/biome-helix-horizontal.png" alt="Biome Logo" height="100px">
          <p>Hi! I'm your Biome Agent and I can help you do all sorts of tasks related to biomedical research. I'm
          particularly good at helping with information retrieval, data analysis, and data visualization. I have 
          access to a wide range of data sources and APIs including GDC, cBioPortal, and more.</p>
        </div>"""
    )
