#Blender Scenes


##Structure:
Each scene have the following structure:

1. 'assets': Contains Blender objects (.blend files) used in scene creation.
2. 'textures': Holds texture files (.png, .jpg) applied to objects in the scenes.
3. 'json_files': Contains JSON files, each corresponding to an image, with information about the objects, their positions, rotations, scales, and textures.
4. 'scripts': Contains Python scripts that load assets from JSON files and render images for each scene.
5. 'outputs': Stores the rendered images of the generated scenes.
6. 'bkg': Holds the HDRI used as backgrounds for scenes.
7. 'annotations': Contains json files for each rendered image
8. 'SBATCH' script to run the python scripts

I added comments for each first script in each scene

##Instructions:

To generate the images customize the directory path in the "scripts","json_files" folders and in the SBATCH files.
You can either execute the "allscenes.sbatch" file, which combines all the sbatch files, or run each sbatch file individually.
