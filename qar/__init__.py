__version__ = "0.0.2"

bl_info = {
    "name": "Quadruped Animation Retargeting (QAR) Tools",
    "blender": (3, 1, 0),
    "category": "Animation",
    "author" : "Arlin Tawzer",
    "location": "3D Viewport",
    "category": "Animation",
}

from .qar_widget import register as register_qar_widget, unregister as unregister_qar_widget

def register():
    register_qar_widget()

def unregister():
    unregister_qar_widget()

if __name__ == "__main__":
    register()