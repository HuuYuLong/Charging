[TOC]

# Charging | Automatically return to port for charging

This  is the source code for  Charging.

run  files `python charging/MainStateMachine.py` to start automatically return to port for charging.

## Structure

This source code consists of:

- **ArucoPoseEstimation** : Use for detect the ArUco marker and the color charging pile.
- **BodyMove.py** : Use for control mars move.
- **ChargingStrategy** : All of the different behavior on different distance (Long, Mid, Close) strategy.
- **MainStateMachine** : The finite state machine use for  control  different strategy of behavior when cats in different states.
- **test_BodyMove** : Use for test BodyMove.py

Next is the details of each module

---

### ArucoPoseEstimation.py

Class:   

-  `ArucoPoseEstimation(object)`

  function:

  `__init__`  :  

  - Use for initialize parameters, the camera x, y, z direction is right, down and out  in respectively.
- `self.PoseData = [x, y, z, pitch]` ，here x, y, z unit is (cm) ,when facing marker x direction is right, y direction is up, z direction is toward us.
  -  `self.colorPileData = [x, y]` , here is the detect color pile of charging, and the x, y is position of color pile, and x direction is right, and y direction is up.

  `_isRotationMatrix`  :

  - Checks if matrix is a valid rotation matrix, use for next function.
- *:param* R :    rotation matrix
  - *:return* :    return True of False

  `_rotationMatrixToEulerAngles`  :
  
  - Calculates rotation matrix to Euler angles.
  - *:param* R :    rotation matrix.
  - *:return* :   `np.array([roll, pith, yaw])` .
  
  `_flipFrame`  :
  
  - Image mirrors.
  - *:param* frame :    Image frame.
  - *:param* flipCode :    1 (horizontal), 0 (vertical), -1 (both horizontally and vertically).
  - *:return* :    Image frame after flip.
  
  `_detect`  :
  
  - Show the Axis of aruco marker and return the x, y, z  in time. (unit is cm).
  - *:param* corners :    get from `cv2.aruco.detectMarkers()` .
  - *:param* ids :    get from `cv2.aruco.detectMarkers()` .
  - *:param* imgWithAruco :    assign imRemapped_color to imgWithAruco directly.
  - *:return* :    x, y, z (units is cm), roll, pitch, yaw (units is degree).
  
  `getPoseData`  :
  
  - Get the data of Position is time.
  - *:return* : `self.PoseData` .
  
  `getColorPileData`  :
  
  - Get the data of the Position of charging pile.
  - *:return* : `self.colorPileData`



---

### BodyMove.py

Class:   

- `BodyMove(object)`

  function:

  `__init__`  :

  - Initialize the parameters. have the range of head degree list and init the data of Voltage.

  `headUpOneStep`  :

  - Rise head one step.

  `haedDownOneStep`  :

  - Down head one step.

  `turnLeftOneStep`  :

  - Turn left one step.
  - *:param* step :    range is [3, 15]. Unit is degrees. 
  - *:param* speed :    range is [0.1, 1].

  `turnRightOneStep`  :

  - Turn right one step.
  - *:param* step :    range is [3, 15]. Unit is degrees. 
  - *:param* speed :    range is [0.1, 1].

  `goOneStep`  :

  - Go forward one step. Trot(1)  ->  Trot(2)  ->  Trot(0).
  - *:param* step :    range is [0.005, 0.04]. Unit is meters. 
  - *:param* delay:    Unit is second. 

  `backOneStep`  :

  - Back one step. Trot(1)  ->  Trot(2)  ->  Trot(0).
  - *:param* step :    range is [0.005, 0.04]. Unit is meters. 
  - *:param* delay:    Unit is second. 

  `leftMoveOneStep`  :

  - Left move one step in horizontal. Trot(1)  ->  Trot(2)  ->  Trot(0).
  - *:param* step :    range is [0.005, 0.04]. Unit is meters. 
  - *:param* delay:    Unit is second. 

  `rightMoveOneStep`  :

  - Right move one step in horizontal. Trot(1)  ->  Trot(2)  ->  Trot(0).
  - *:param* step :    range is [0.005, 0.04]. Unit is meters. 
  - *:param* delay:    Unit is second. 

  `getTof`  :

  - Get the the distance data of Tof in time.
  - *:return* :    The distance data, unit is (mm).

  `headInit`  :

  - Use for initialize the head angles.

  `staticPose`  :

  - Use for initialize the static pose.

  `sitDown` :

  - The sit down use for charging.
  - *** TODO need improve and test**.

  `chargeCharging`  :

  - Judge whether in charge.
  - *:return* :    True or False.

 

---

### ChargingStrategy.py

class:

- `ChargingStrategy(object)`  

  function:

  `__init__`  :

  - Initialize the parameters
  - `self.PoseData = [x, y, z, pitch]` ,get from `ArucoPoseEstimation.getPoseData()` ,here x, y, z unit is (cm) ,when facing marker x direction is right, y direction is up, z direction is toward us.
  -  `self.colorPileData = [x, y]` , get from `ArucoPoseEstimation.getColorPileData()` , here is the detect color pile of charging, and the x, y is position of color pile, and x direction is right, and y direction is up.
  - `self.ObstacleData = xxxx`, get from `BodyMove.getTof()`, unit is (mm).
  - `self.lastDetect = left or right` , save the last direction of target.

  `_getPoseColorPileData`  :

  - Tread to get current ArUco Marker data and color charging pile data.

  `_detectObstacle`  :

  - Tread to get current Tof distance data.

  `_detectArucoPile`  :

  - Start CAMERA thread, getPoseColorPileData thread and detectObstacle thread.

  

  `wandering`  :

  - Robotics random wandering when can't find target.
  - ***TODO need improve and test**

  `walkAwayObstacle`  :

  - Getting out of the obstacles when face obstacles.
  - ***TODO need improve and test**

  `obstacleAvoidanceWalk`  :

  - Walking with avoid obstacle when get target and face obstacle.
  - ***TODO need importve**

  `findTargetInSitu`  :

  - Finding target in situ when lost target.

  `walk2Center`  :

  - Walking towards ArUco marker center.

  `longGetObstacleTargetData`  :

  - Obtain obstacle and target data when long distance.

  - *:return* :   

    - "q"  end long distance strategy state.

    - "00" if not lost target and no obstacle state.

    - "01" if not lost target and have obstacle state.

    - "10" if lost target and no obstacle state.

    - "11" if lost target and have obstacle state.

  

  `ajustPose`  :

  - Adjusting the cat to the front of the center of the Aruco marker.

  `midGetTargetData`  :

  - Obtain obstacle and target data when mid distance.
  - *:return* :   
    - "q" end mid distance strategy
    - "1" Adjusting the cat to the front of the center of the ArUco marker



---

### MainStateMachine.py

class:

- `longTestState(LongStrategeState)`

  function:

  `__init__`  :    `self.name = "TestState"` .

  `exec`  :    

  - Get return data from `longGetObstacleTargetData()` .

  `exit`  :

  - *:return* :   
    - 1 if data = "00",  
    - 3 if data = "01", 
    - 2 if data = "10", 
    - 4 if data = "11", 
    - 5 if data = "q"  .

class:

- `NLostT_NObstacle(LongStrategeState)`

  function: 

  `__init__`  :   

  -  `self.name = "NLostT_NObstacle" `.

  `exec`  :   

  -  Run function `walk2Center()` .

  `exit`  :   

  - *:return* :    ` 0`, go into the test state.

class:

- `LostT_NObstacle(LongStrategeState)`

  function:

  `__init__`  :    

  - `self.name = "LostT_NObstacle"`

  `exec`  :    
  
  - Run function `findTargetInSitu()` first, if not find than run function `wandering()` .
  
  `exit`  :  
  
  - *:return* :     ` 0`, go into the test state.

class:

- `NLostT_Obstacle(LongStrategeState)`

  function:

  `__init__`  :

  - `self.name = "NLostT_Obstacle"`. 

  `exec` :

  - In this state run function`obstacleAvoidanceWalk()`.

  `exit`  :   

  - *:return* :    ` 0`, go into the test state.

class:

- `LostT_Obstacle(LongStrategeState)`

  function:

  `__init__`  :

  - `self.name = "LostT_Obstacle"` .

  `exec`  :
  
  - In this state run function `walkAwayObstacle()`.
  
  `exit`  :   
  
  - *:return* :    ` 0`, go into the test state.

---

class:

- `midTestState(MidStrategeState)`

  function:

  `__init__`  :

  - `self.name = "TestState"`

  `exec`  :    

  - In this state run function `midGetTargetData()` . and get the test state data.

  `exit`  :    

  - *:return* :   
    - 1 if data = "1",  
    - 5 if data = "q"  .

class:

- `notFacetoMarker(MidStrategeState)`

  function:

  `__init__`  :

  - `self.name = "notFacetoMarker"`

  `exec`  :

  - In this state run function `ajustPose()`

  `exit`  :

  - *:return* :    ` 0`, go into the test state.

class:

- `Finished(State)`

  function:

  `__init__`  :

  - `self.name = "Finished"`

  `exec`  :    Nothing

  `exit`  :    Nothing

-----

class:

- `StateMachine(object)`

  function:

  `__init__`:

  - That is finite state  machine, control  different strategy of behavior when cats in different states. But close States behavior coding in `main()`.
  - `self.longStates`  :    Define long distance States.
    - `0: longTestState()`
    - `1: NLostT_NObstacle()`
    - `2: LostT_NObstacle()`
    - `3: NLostT_Obstacle()`
    - `4: LostT_Obstacle()`
    - `5: Finished()`
  - `self.midStates`  :    Define mid distance States.
    - `0: midTestState()`
    - `1: notFacetoMarker()`
    - `5: Finished()`

  `AutoRun`  :

  - Auto run the finite state machine until robot charging complete.

---

**Main function: `main()`** 



### test_BodyMove.py

Use for test `BodyMove.py`

## Libraries

Pre-installed libraries includes OpenCV 3,  Pyfirmata.

