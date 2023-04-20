import bpy
import math

class TurnCircleSettings(bpy.types.PropertyGroup):
    turn_angle: bpy.props.FloatProperty(name="Turn Angle", default=15)
    chest_rotation_multiplier: bpy.props.FloatProperty(name="Chest Rotation Multiplier", default=0.9)
    neck_rotation_multiplier: bpy.props.FloatProperty(name="Neck Rotation Multiplier", default=-1)
    head_rotation_multiplier: bpy.props.FloatProperty(name="Head Rotation Multiplier", default=-1.5)
    foot_rotation_multiplier: bpy.props.FloatProperty(name="Foot Rotation Multiplier", default=1)
    foot_x_offset: bpy.props.FloatProperty(name="Foot Offset Multiplier", default=0)

    # UI properties
    turn_circle_panel_expanded: bpy.props.BoolProperty(default=True)


class TurnCircleOperator(bpy.types.Operator):
    bl_idname = "object.create_turn_circle"
    bl_label = "Create Turn Circle Actions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        # Housekeeping
        self.armature_obj = bpy.data.objects[context.scene.arte_settings.armature_name]
        self.source_action_name = context.object.animation_data.action.name
        self.turn_angle = context.scene.turn_circle_settings.turn_angle
        self.foot_prefix = context.scene.arte_settings.foot_prefix
        self.turn_bones = [
            context.scene.arte_settings.chest_bone,
            context.scene.arte_settings.neck_bone,
            context.scene.arte_settings.head_bone,
            f"{context.scene.arte_settings.foot_prefix}.R",
            f"{context.scene.arte_settings.foot_prefix}.L",
        ]

        # How much to modify each one
        self.turn_angle_multipliers = {
            'chest': context.scene.turn_circle_settings.chest_rotation_multiplier,
            'neck': context.scene.turn_circle_settings.neck_rotation_multiplier,
            'head': context.scene.turn_circle_settings.head_rotation_multiplier,
            f"{context.scene.arte_settings.foot_prefix}.R": context.scene.turn_circle_settings.foot_rotation_multiplier,
            f"{context.scene.arte_settings.foot_prefix}.L": context.scene.turn_circle_settings.foot_rotation_multiplier,
        }

        # Whether we want to move the feet as well
        self.foot_x_offset = context.scene.turn_circle_settings.foot_x_offset

        self.create_turn_circle_actions()
        return {'FINISHED'}
    
    def create_turn_circle_actions(self):
        """
        Based on the current active action, will create .R and .L actions
        and apply the turn circle to them.
        """
        source_action = bpy.data.actions[self.source_action_name]

        # Create or reuse left turn action
        left_turn_action_name = f"{self.source_action_name}.L"
        left_turn_action = bpy.data.actions.get(left_turn_action_name)
        if left_turn_action is None:
            left_turn_action = source_action.copy()
            left_turn_action.name = left_turn_action_name
        else:
            self.copy_action_data(source_action, left_turn_action)

        self.apply_turn_circle(left_turn_action)

        # Create or reuse right turn action
        right_turn_action_name = f"{self.source_action_name}.R"
        right_turn_action = bpy.data.actions.get(right_turn_action_name)
        if right_turn_action is None:
            right_turn_action = source_action.copy()
            right_turn_action.name = right_turn_action_name
        else:
            self.copy_action_data(source_action, right_turn_action)

        self.apply_turn_circle(right_turn_action, invert=True)

    @staticmethod
    def copy_action_data(action1, action2):
        """
        Copies the data from one action to another.
        """

        # Clear the F-curves in action2
        for fc in action2.fcurves:
            action2.fcurves.remove(fc)

        # Copy the F-curves from action1 to action2
        for fc in action1.fcurves:
            group_name = fc.group.name if fc.group is not None else ""
            new_fc = action2.fcurves.new(fc.data_path, index=fc.array_index, action_group=group_name)
            new_fc.keyframe_points.add(count=len(fc.keyframe_points))
            for kfp in fc.keyframe_points:
                new_kfp = new_fc.keyframe_points[-1]
                new_kfp.co = kfp.co[:]
                new_kfp.handle_left = kfp.handle_left[:]
                new_kfp.handle_right = kfp.handle_right[:]
                new_kfp.interpolation = kfp.interpolation

        # Copy the use_fake_user property from action1 to action2
        action2.use_fake_user = action1.use_fake_user


    def apply_turn_circle(self, action, invert=False):
        """
        Predominant method for actually performing the turn circle.
        """
        self.rotate_bones(action, invert=invert)
        self.adjust_foot_movement(action)  # Replace 'forefoot_' with the correct prefix for the foot bones

        # Assign the modified action to the armature
        self.armature_obj.animation_data_create()
        self.armature_obj.animation_data.action = action
    
    def rotate_bones(self, action, invert=False):
        """
        Rotates the bones according to the turn angle and multipliers.
        """
        turn_angle_rad = math.radians(self.turn_angle) if not invert else -math.radians(self.turn_angle)
        
        for fcurve in action.fcurves:
            bone_name = fcurve.data_path.split('"')[1] if 'pose.bones' in fcurve.data_path else None
            if bone_name in self.turn_bones and fcurve.array_index == 3:  # Array index 3 corresponds to Quat.Z rotation
                for keyframe in fcurve.keyframe_points:
                                
                    bone_turn_angle = turn_angle_rad * self.turn_angle_multipliers.get(bone_name, 1)
                    
                    keyframe.co.y += bone_turn_angle
                    keyframe.handle_left.y += bone_turn_angle
                    keyframe.handle_right.y += bone_turn_angle


    def adjust_foot_movement(self, action):
        """
        Adjusts the feet (which are rotated above) to move on an angle.
        """
        foot_bones = [bone for bone in self.armature_obj.pose.bones if bone.name.startswith(self.foot_prefix)]
        
        for foot_bone in foot_bones:
            self.adjust_foot_speed(action, foot_bone)


    def adjust_foot_speed(self, action, foot_bone):
        """
        Performs the actual foot movement adjustment.
        """

        turn_angle_rad = math.radians(self.turn_angle)
        cos_turn = math.cos(turn_angle_rad)
        sin_turn = math.sin(turn_angle_rad)

        x_fcurve = None
        y_fcurve = None

        for fcurve in action.fcurves:
            if f'pose.bones["{foot_bone.name}"].location' in fcurve.data_path:
                if fcurve.array_index == 0:
                    x_fcurve = fcurve
                elif fcurve.array_index == 1:
                    y_fcurve = fcurve

        if x_fcurve and y_fcurve:
            for x_key, y_key in zip(x_fcurve.keyframe_points, y_fcurve.keyframe_points):
                # Compute new x and y values
                new_x = cos_turn * x_key.co.y - sin_turn * y_key.co.y
                new_y = sin_turn * x_key.co.y + cos_turn * y_key.co.y
                x_offset = self.foot_x_offset if '.R' in action.name else -self.foot_x_offset

                new_x = new_x * -1 if '.R' in action.name else new_x
                x_key.co.y += new_x + x_offset
                y_key.co.y = new_y

                # Adjust Bezier handles
                new_left_x = cos_turn * x_key.handle_left.y - sin_turn * y_key.handle_left.y
                new_right_x = cos_turn * x_key.handle_right.y - sin_turn * y_key.handle_right.y

                new_left_x, new_right_x = (new_left_x * -1 if '.R' in action.name else new_left_x, 
                                           new_right_x * -1 if '.R' in action.name else new_right_x)

                x_key.handle_left.y = new_left_x + x_offset
                y_key.handle_left.y = sin_turn * x_key.handle_left.y + cos_turn * y_key.handle_left.y

                x_key.handle_right.y = new_right_x + x_offset
                y_key.handle_right.y = sin_turn * x_key.handle_right.y + cos_turn * y_key.handle_right.y

######################
### ARTE Functions ###
######################
def draw(layout, context):
    settings = context.scene.turn_circle_settings

    col = layout.column()
    row = col.row()
    row.prop(settings, "turn_circle_panel_expanded", text="Turn Circle", icon='TRIA_DOWN' if settings.turn_circle_panel_expanded else 'TRIA_RIGHT', emboss=False)

    if settings.turn_circle_panel_expanded:

        col.prop(settings, "turn_angle")   
        col.prop(settings, "chest_rotation_multiplier")
        col.prop(settings, "neck_rotation_multiplier")
        col.prop(settings, "head_rotation_multiplier")
        col.prop(settings, "foot_rotation_multiplier")
        col.prop(settings, "foot_x_offset")
        col.operator("object.create_turn_circle")



def register():
    bpy.utils.register_class(TurnCircleSettings)
    bpy.types.Scene.turn_circle_settings = bpy.props.PointerProperty(type=TurnCircleSettings)
    bpy.utils.register_class(TurnCircleOperator)


def unregister():
    bpy.utils.unregister_class(TurnCircleSettings)
    del bpy.types.Scene.turn_circle_settings
    bpy.utils.unregister_class(TurnCircleOperator)