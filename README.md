# URDF_Visualizer_PyBullet
Script using PyBullet to visualize URDFs.
Good for quick testing of a URDF that you are making insuring that your translations/rotations are correct as well as the joint type and limits.


## Requirements:
* Python3
* PyBullet, Install:
    ```console,
    pip3 install pybullet
    ```
* tk, Install:
    ```console,
    sudo apt install python3-tk
    ```


## How to use:

* Run URDF_Visulizer.py
* With the pop up window select navigate and select the URDF file that you want to visualize
* A PyBullet window will open showing your robot and on the right will be sliders that control each of the joints.