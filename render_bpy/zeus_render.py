import bpy
import math

import os
import sys
import contextlib
@contextlib.contextmanager
def stdout_redirect(to=os.devnull):
    fd = sys.stdout.fileno()

    def redirect_stdout(to):
        sys.stdout.close()
        os.dup2(to.fileno(), fd)
        sys.stdout = os.fdopen(fd, 'w')

    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open(to, 'w') as file:
            redirect_stdout(to=file)
        try:
            yield
        finally:
            redirect_stdout(to=old_stdout) 

def calculate_camera_position_and_rotation(center, radius, number):
    import mathutils
    position_rotation = []    
    for i in range(number):
        angle = (2 * math.pi * i / number) - (2 * math.pi / number)
        position = (center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle), center[2])
        rotation = (mathutils.Vector(position) - mathutils.Vector(center)).to_track_quat('Z', 'Y').to_euler()
        position_rotation.append([position, (rotation.x, rotation.y, rotation.z)])
    return position_rotation

def render(file_i, path_o):
    import os; os.makedirs(os.path.dirname(path_o), exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)

    with stdout_redirect():
        bpy.ops.import_scene.fbx(filepath=file_i)  
    frame_total = int(bpy.context.active_object.animation_data.action.frame_range[1])

    new_light_position_direction = [[(0.0,-5.0,0.9),(90,0,0)],[(5.0,0.0,0.9),(90,0,90)],[(0.0,5.0,0.9),(-90,180,0)],[(-5.0,0.0,0.9),(90,0,-90)]]
    for position,direction in new_light_position_direction:
        bpy.ops.object.light_add(type='SUN')
        new_light = bpy.context.object
        new_light.data.energy = 3.0
        new_light.location = position
        new_light.rotation_euler = (math.radians(direction[0]), math.radians(direction[1]), math.radians(direction[2]))
    
    position_rotation = calculate_camera_position_and_rotation(center=(0.0,0.0,0.9), radius=5, number=frame_total)
    bpy.ops.object.camera_add()
    new_camera = bpy.context.object
    bpy.context.scene.camera = new_camera

    bpy.context.scene.render.engine = ['CYCLES','EEVEE'][0]
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.resolution_x = 800
    bpy.context.scene.render.resolution_y = 800
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frame_total 

    for index in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        filepath = os.path.join(os.getcwd(), path_o, os.path.basename(os.path.split(file_i)[0])+' #$# '+os.path.splitext(os.path.split(file_i)[1])[0], "{:08d}".format(index))
        filename = filepath+'.png'
        if not os.path.exists(filename):
            camera = bpy.context.scene.camera
            camera.location = position_rotation[index-1][0]
            camera.rotation_euler = position_rotation[index-1][1]
            bpy.context.scene.frame_set(index)
            bpy.context.scene.render.filepath = filepath
            with stdout_redirect():
                bpy.ops.render.render(write_still=True)
            print('render: done %08d/%08d  %s    %s'%(index,frame_total, file_i, filename))
        else:
            print('render: skip %08d/%08d  %s    %s'%(index,frame_total, file_i, filename))

def main(path_o='../data/image/motion/'):
    #render(file_i='../data/mixamo/The Boss/Boxing.fbx', path_o=path_o)
    #render(file_i='../data/mixamo/The Boss/Throw.fbx', path_o=path_o)
    #render(file_i='../data/mixamo/Maria J J Ong/Aiming.fbx', path_o=path_o)
    #render(file_i='../data/mixamo/Maria W#Prop J J Ong/Closing.fbx', path_o=path_o)
    #render(file_i='../data/mixamo/Mutant/Counting.fbx', path_o=path_o)
    render(file_i='../data/mixamo/Exo Gray/Floating.fbx', path_o=path_o)

if __name__ == '__main__':
    main()
