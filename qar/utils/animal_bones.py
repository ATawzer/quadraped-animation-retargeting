# ====================================
# Allows for quick adjustment of default settings based on the 
# rigify defaults for the Horse, Cat and Dog rigs.
# ====================================

import bpy

class QAR_OT_SetHorseBones(bpy.types.Operator):
    bl_idname = "qar.sethorsebones"
    bl_label = "Set Horse Bones"

    def execute(self, context):
        context.scene.qar_settings.foot_prefix = "forefoot_ik"
        context.scene.qar_settings.back_foot_prefix = "hind_foot_ik"
        return {'FINISHED'}

class QAR_OT_SetCatBones(bpy.types.Operator):
    bl_idname = "qar.setcatbones"
    bl_label = "Set Cat Bones"

    def execute(self, context):
        context.scene.qar_settings.foot_prefix = "hand_ik"
        context.scene.qar_settings.back_foot_prefix = "foot_ik"
        return {'FINISHED'}

class QAR_OT_SetDogBones(bpy.types.Operator):
    bl_idname = "qar.setdogbones"
    bl_label = "Set Dog Bones"

    def execute(self, context):
        context.scene.qar_settings.foot_prefix = "front_foot_ik"
        context.scene.qar_settings.back_foot_prefix = "foot_ik"
        return {'FINISHED'}