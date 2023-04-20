import bpy

def clean_nla_tracks():
    for track in bpy.context.object.animation_data.nla_tracks:
        if len(track.strips) > 0:
            first_strip = track.strips[0]
            track.name = first_strip.action.name