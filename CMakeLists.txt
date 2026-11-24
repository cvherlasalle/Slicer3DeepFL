cmake_minimum_required(VERSION 3.20.6...3.22.6 FATAL_ERROR)

project(3DeepFL)

#-----------------------------------------------------------------------------
# Extension meta-information (keep in sync with README.md and Extensions Index JSON)
set(EXTENSION_HOMEPAGE "https://github.com/cvherlasalle/Slicer3DeepFL#readme")
set(EXTENSION_CONTRIBUTORS "Alexandre Contreras Urbita (La Salle - Universitat Ramon Llull, Spain)")
set(EXTENSION_DESCRIPTION "3DeepFL predicts 3D facial landmarks on surface meshes using local MVCNN models, and includes a module to align meshes to the models' reference space. MIT-licensed, with optional CUDA acceleration and on-demand model downloads; no related patents are known.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/cvherlasalle/Slicer3DeepFL/main/icon.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/cvherlasalle/Slicer3DeepFL/main/Screenshots/standardization_before.png https://raw.githubusercontent.com/cvherlasalle/Slicer3DeepFL/main/Screenshots/standardization_after.png https://raw.githubusercontent.com/cvherlasalle/Slicer3DeepFL/main/Screenshots/landmarking_after.png")
set(EXTENSION_DEPENDS "NA") 

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(AutomatedLandmarking)
add_subdirectory(FaceStandardization)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
