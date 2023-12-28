import bpy
import random
import math
import mathutil

# Set the frame range
start_frame = 1
end_frame = 3600

# Your objects (empty planes)
object1 = bpy.data.objects["empty.001"]
object2 = bpy.data.objects["empty.002"]

# Starting location and rotation
original_loc1 = object1.location.copy()
original_rot1 = object1.rotation_euler.copy()
original_loc2 = object2.location.copy()
original_rot2 = object2.rotation_euler.copy()

# Frame start and end (scene)
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = end_frame

# Random motions
def random_motion(obj, frame, original_loc, original_rot):
    bpy.context.scene.frame_set(frame)
    obj.location = original_loc + mathutils.Vector((random.uniform(-3, 3), random.uniform(-3, 3), 0))
    # Convert original rotation to Quaternion
    original_rot_quat = original_rot.to_quaternion()
    # New rotation as Quaternion
    delta_rotation = mathutils.Euler((0, random.uniform(-math.radians(180), math.radians(180)), 0), 'XYZ').to_quaternion()
    # Combine rotations and convert back to Euler
    obj.rotation_euler = (original_rot_quat * delta_rotation).to_euler
 
    obj.keyframe_insert(data_path="location", index=-1)
    obj.keyframe_insert(data_path="rotation_euler", index=-1)

# Insert keyframes with interpolation
def set_interpolation(obj):
    if obj.animation_data and obj.animation_data.action:
        fcurves = bpy.context.object.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER' # 'BEZIER', 'CONSTANT', 'QUARTIC', 'BOUNCE' etc
    else:
        print(f"No animation data found for {obj.name}")

# Inserting keyframes
for f in range(start_frame, end_frame, 240): # Change 30 to 90, 180 or any other value to set keyframe intervalls
    random_motion(object1, f, original_loc1, original_rot1)
    random_motion(object2, f, original_loc2, original_rot2)

# Set interpolation for the empties
set_interpolation(object1)
set_interpolation(object2)

# Return empties to original pos / rot
random_motion(object1, end_frame, original_loc1, original_rot1)
random_motion(object2, end_frame, original_loc2, original_rot2)