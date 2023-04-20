# UI
from .turn_circle import draw as turn_circle_draw
from .foot_controller import draw as foot_controller_draw

# Register the turn circle operator
from .turn_circle import register as turn_circle_register, unregister as turn_circle_unregister
from .foot_controller import register as foot_controller_register, unregister as foot_controller_unregister

import bpy
import math

class QARSettings(bpy.types.PropertyGroup):
    chest_bone: bpy.props.StringProperty(name="Chest Bone", default="chest")
    neck_bone: bpy.props.StringProperty(name="Neck Bone", default="neck")
    head_bone: bpy.props.StringProperty(name="Head Bone", default="head")
    foot_prefix: bpy.props.StringProperty(name="Foot Prefix", default="forefoot_ik")
    back_foot_prefix: bpy.props.StringProperty(name="Back Foot Prefix", default="hind_foot_ik")
    armature_name: bpy.props.StringProperty(name="Armature Name", default="SK_Horse")

class QAR_PT_Panel(bpy.types.Panel):
    bl_label = "QAR"
    bl_idname = "OBJECT_PT_QAR"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "QAR"

    def draw(self, context):
        layout = self.layout

        # QAR Settings
        qar_settings_box = layout.box()
        qar_settings_box.label(text="Rig Settings")
        qar_settings_box.prop(context.scene.qar_settings, "armature_name")
        qar_settings_box.prop(context.scene.qar_settings, "chest_bone")
        qar_settings_box.prop(context.scene.qar_settings, "neck_bone")
        qar_settings_box.prop(context.scene.qar_settings, "head_bone")
        qar_settings_box.prop(context.scene.qar_settings, "foot_prefix")
        qar_settings_box.prop(context.scene.qar_settings, "back_foot_prefix")

        # Turn Circles
        turn_circle_box = layout.box()
        turn_circle_draw(turn_circle_box, context)

        # Foot Spacing and Stride Length
        foot_controller_box = layout.box()
        foot_controller_draw(foot_controller_box, context)

def register():

    bpy.utils.register_class(QARSettings)
    bpy.types.Scene.qar_settings = bpy.props.PointerProperty(type=QARSettings)

    turn_circle_register()
    foot_controller_register()

    bpy.utils.register_class(QAR_PT_Panel)

def unregister():
    turn_circle_unregister()
    foot_controller_unregister()

    bpy.utils.unregister_class(QAR_PT_Panel)

    del bpy.types.Scene.qar_settings
    bpy.utils.unregister_class(QARSettings)

if __name__ == "__main__":
    register()