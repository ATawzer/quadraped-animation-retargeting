# UI
from .turn_circle import draw as turn_circle_draw
from .foot_controller import draw as foot_controller_draw

# Register the turn circle operator
from .turn_circle import register as turn_circle_register, unregister as turn_circle_unregister
from .foot_controller import register as foot_controller_register, unregister as foot_controller_unregister

# Helper Operators
from .utils import QAR_OT_SetHorseBones, QAR_OT_SetCatBones, QAR_OT_SetDogBones, QAR_OT_CleanNlaTracks

import bpy
import math

def update_armature(self, context):
    armature = bpy.data.objects.get(self.armature_name)
    # Add any code you want to execute when the armature is updated
    # For example, update the bone names based on the selected armature

class QARSettings(bpy.types.PropertyGroup):

    def armature_items(self, context):
        return [(ob.name, ob.name, "") for ob in bpy.data.objects if ob.type == 'ARMATURE']

    # Defaults for the horse
    chest_bone: bpy.props.StringProperty(name="Chest Bone", default="chest")
    neck_bone: bpy.props.StringProperty(name="Neck Bone", default="neck")
    head_bone: bpy.props.StringProperty(name="Head Bone", default="head")
    foot_prefix: bpy.props.StringProperty(name="Foot Prefix", default="forefoot_ik")
    back_foot_prefix: bpy.props.StringProperty(name="Back Foot Prefix", default="hind_foot_ik")
    armature_name: bpy.props.EnumProperty(
        name="Armature",
        description="Select the armature",
        items=armature_items,
        update=update_armature,
    )

class QAR_PT_Panel(bpy.types.Panel):
    bl_label = "QAR"
    bl_idname = "OBJECT_PT_QAR"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "QAR"

    def draw(self, context):
        layout = self.layout

        # Animal Buttons
        animal_buttons_box = layout.box()
        animal_buttons_box.label(text="Animal Rig Presets")
        animal_buttons_box.operator(QAR_OT_SetHorseBones.bl_idname, text="Horse")
        animal_buttons_box.operator(QAR_OT_SetCatBones.bl_idname, text="Cat")
        animal_buttons_box.operator(QAR_OT_SetDogBones.bl_idname, text="Dog")

        # QAR Settings
        qar_settings_box = layout.box()
        qar_settings_box.label(text="Rig Settings")
        qar_settings_box.prop(context.scene.qar_settings, "armature_name")
        qar_settings_box.prop(context.scene.qar_settings, "chest_bone")
        qar_settings_box.prop(context.scene.qar_settings, "neck_bone")
        qar_settings_box.prop(context.scene.qar_settings, "head_bone")
        qar_settings_box.prop(context.scene.qar_settings, "foot_prefix")
        qar_settings_box.prop(context.scene.qar_settings, "back_foot_prefix")
        qar_settings_box.operator(QAR_OT_CleanNlaTracks.bl_idname, text="Clean NLA Tracks")


        # Turn Circles
        turn_circle_box = layout.box()
        turn_circle_draw(turn_circle_box, context)

        # Foot Spacing and Stride Length
        foot_controller_box = layout.box()
        foot_controller_draw(foot_controller_box, context)

def register():

    bpy.utils.register_class(QARSettings)
    bpy.utils.register_class(QAR_OT_SetHorseBones)
    bpy.utils.register_class(QAR_OT_SetCatBones)
    bpy.utils.register_class(QAR_OT_SetDogBones)
    bpy.utils.register_class(QAR_OT_CleanNlaTracks)
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
    bpy.utils.unregister_class(QAR_OT_SetHorseBones)
    bpy.utils.unregister_class(QAR_OT_SetCatBones)
    bpy.utils.unregister_class(QAR_OT_SetDogBones)
    bpy.utils.unregister_class(QAR_OT_CleanNlaTracks)

if __name__ == "__main__":
    register()