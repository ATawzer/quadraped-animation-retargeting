import bpy

class QAR_OT_CleanNlaTracks(bpy.types.Operator):
    bl_idname = "qar.clean_nla_tracks"
    bl_label = "Clean NLA Tracks"
    bl_description = "Clean NLA tracks based on their first strip's action name"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.clean_nla_tracks(context)
        return {'FINISHED'}
    
    @staticmethod
    def clean_nla_tracks(context):
        for track in context.object.animation_data.nla_tracks:
            if len(track.strips) > 0:
                first_strip = track.strips[0]
                track.name = first_strip.action.name