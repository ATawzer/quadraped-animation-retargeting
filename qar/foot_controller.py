import bpy

def draw(layout, context):
    settings = context.scene.foot_controller_settings

    col = layout.column()
    row = col.row()
    row.prop(settings, "foot_controller_settings_expanded", text="Foot Controller", icon='TRIA_DOWN' if settings.foot_controller_settings_expanded else 'TRIA_RIGHT', emboss=False)

    if settings.foot_controller_settings_expanded:

        col = layout.column(align=True)
        col.label(text="Stride Length Options:")
        col.prop(settings, "front_scale_factor")
        col.prop(settings, "hind_scale_factor")

        col = layout.column(align=True)
        col.label(text="Stride Positioning Options:")
        col.prop(settings, "front_translation_amount")
        col.prop(settings, "hind_translation_amount")

        col = layout.column(align=True)
        col.operator("object.scale_and_translate_keyframes", text="Scale and Translate Keyframes")
        col.operator("object.reset_scale_and_translate_values", text="Reset")


class OBJECT_OT_scale_and_translate_keyframes(bpy.types.Operator):
    bl_label = "Scale and Translate Keyframes"
    bl_idname = "object.scale_and_translate_keyframes"

    def execute(self, context):
        front_foot_bone_names = [f"{context.scene.qar_settings.foot_prefix}.R", 
                                 f"{context.scene.qar_settings.foot_prefix}.L"]
        hind_foot_bone_names = [f"{context.scene.qar_settings.back_foot_prefix}.R", 
                                f"{context.scene.qar_settings.back_foot_prefix}.L"]
        front_scale_factor = context.scene.foot_controller_settings.front_scale_factor
        front_translation_amount = context.scene.foot_controller_settings.front_translation_amount
        hind_scale_factor = context.scene.foot_controller_settings.hind_scale_factor
        hind_translation_amount = context.scene.foot_controller_settings.hind_translation_amount
        armature_name = context.scene.qar_settings.armature_name

        # Scale and translate front foot keyframes
        scale_and_translate_keyframes(
            front_foot_bone_names,
            front_scale_factor,
            front_translation_amount,
            armature_name
        )

        # Scale and translate hind foot keyframes
        scale_and_translate_keyframes(
            hind_foot_bone_names,
            hind_scale_factor,
            hind_translation_amount,
            armature_name
        )

        reset_options(context)
        
        return {'FINISHED'}
    
class OBJECT_OT_reset_scale_and_translate_values(bpy.types.Operator):
    bl_label = "Reset Scale and Translate Values"
    bl_idname = "object.reset_scale_and_translate_values"

    def execute(self, context):
        reset_options(context)
        return {'FINISHED'}

def reset_options(context):
    context.scene.foot_controller_settings.front_scale_factor = 1.0
    context.scene.foot_controller_settings.front_translation_amount = 0.0
    context.scene.foot_controller_settings.hind_scale_factor = 1.0
    context.scene.foot_controller_settings.hind_translation_amount = 0.0

def scale_and_translate_keyframes(bone_names, scale_factor, translation_amount, armature_name):
    armature_obj = bpy.data.objects[armature_name]
    for bone_name in bone_names:
        bone = armature_obj.pose.bones[bone_name]
        action = armature_obj.animation_data.action
        if action:
            for fcurve in action.fcurves:
                if fcurve.data_path == f'pose.bones["{bone_name}"].location' and fcurve.array_index == 1:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.handle_left[1] *= scale_factor
                        keyframe.handle_left[1] += translation_amount

                        keyframe.handle_right[1] *= scale_factor
                        keyframe.handle_right[1] += translation_amount

                        # Scale the keyframe value
                        keyframe.co[1] *= scale_factor
                        # Translate the keyframe value
                        keyframe.co[1] += translation_amount

class FootContollerSettings(bpy.types.PropertyGroup):
    front_scale_factor:bpy.props.FloatProperty(
        name="Front Scale Factor",
        description="The factor to scale the front foot keyframes by",
        default=1.0
    )
    front_translation_amount:bpy.props.FloatProperty(
        name="Front Translation Amount",
        description="The amount to translate the front foot keyframes by",
        default=0.0
    )
    hind_scale_factor:bpy.props.FloatProperty(
        name="Hind Scale Factor",
        description="The factor to scale the hind foot keyframes by",
        default=1.0
    )
    hind_translation_amount:bpy.props.FloatProperty(
        name="Hind Translation Amount",
        description="The amount to translate the hind foot keyframes by",
        default=0.0
    )

    # UI properties
    foot_controller_settings_expanded: bpy.props.BoolProperty(default=True)
              
def register():
    bpy.utils.register_class(FootContollerSettings)
    bpy.types.Scene.foot_controller_settings = bpy.props.PointerProperty(type=FootContollerSettings)

    bpy.utils.register_class(OBJECT_OT_scale_and_translate_keyframes)
    bpy.utils.register_class(OBJECT_OT_reset_scale_and_translate_values)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_scale_and_translate_keyframes)
    bpy.utils.unregister_class(OBJECT_OT_reset_scale_and_translate_values)

    del bpy.types.Scene.foot_controller_settings
    bpy.utils.unregister_class(FootContollerSettings)
    
