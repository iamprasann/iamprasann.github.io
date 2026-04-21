# UMIC_TEAM4-Final

`UMIC_TEAM4-Final` is a ROS/Gazebo robotics project preserved as the final setup for a UMIC recruitment project. Unlike the semester archives and notebook-heavy coursework repos, this repository is clearly a workspace-oriented engineering project: package structure, launch files, URDF assets, controller configs, environment worlds, and Python scripts for perception and control.

## Overview

- Repository: [iamprasann/UMIC_TEAM4-Final](https://github.com/iamprasann/UMIC_TEAM4-Final)
- Created: August 22, 2020
- Updated: August 23, 2020
- Primary language on GitHub: CMake

Top-level structure:

- `src`
- `src_aryan`
- `README.md`

The root README frames the repository as the final setup for the UMIC recruitment project and explicitly calls out `ball_detection` as a working component.

## Why It Mattered

This repository matters because it looks like one of the earliest fully engineering-shaped projects in the corpus. It is not just a set of assignments or reports; it captures:

- a real package-oriented robotics workspace
- simulation and visualization setup via ROS/Gazebo tooling
- perception work through `ball_detection.py`
- robot-description and control configuration assets
- an alternate or earlier workspace tree preserved alongside the final one

That makes it important as evidence of hands-on systems integration work.

## How It Worked

The main final workspace lives under `src`, where two ROS packages, `final_description` and `final_gazebo`, define the robot and simulation environment.

- `final_description` contains launch files for controls, Gazebo, RViz, flaps, gates, and differential drive.
- It also includes YAML controller/joint configuration, URDF/Xacro assets, and Python scripts such as `ball_detection.py`, `pushing_ball.py`, and `laser_distance.py`.
- `final_gazebo` contains the Gazebo launch file and world definition.

The README describes the intended setup as a catkin workflow: create a workspace, build it, adjust the package setup, relaunch, and then run the ball-detection script. The README also notes that the ball-detection path returns center coordinates relative to a `400x400` camera frame, which makes the vision component a concrete project milestone rather than just a placeholder script.

The `src_aryan` directory preserves a second ROS workspace layout with packages like `bot1`, `env`, and signboard packages. That tree looks like an earlier or parallel version of the same project, and it is useful context because it shows the project was not a single flat code drop but evolved through multiple package arrangements.

## Key Artifacts

- [Root README](https://github.com/iamprasann/UMIC_TEAM4-Final/blob/master/README.md)
- [src/final_description](https://github.com/iamprasann/UMIC_TEAM4-Final/tree/master/src/final_description)
- [src/final_gazebo](https://github.com/iamprasann/UMIC_TEAM4-Final/tree/master/src/final_gazebo)
- [src_aryan/bot1](https://github.com/iamprasann/UMIC_TEAM4-Final/tree/master/src_aryan/bot1)
- [src_aryan/env](https://github.com/iamprasann/UMIC_TEAM4-Final/tree/master/src_aryan/env)

Representative artifacts visible in the repo include:

- ROS package manifests and `CMakeLists.txt`
- launch files for controls, Gazebo, RViz, gates, flaps, and differential drive
- YAML configuration files for robot joints and mechanisms
- URDF, Xacro, and Gazebo description assets
- Python scripts for ball detection, image handling, laser distance, and ball pushing
- world files and signboard/environment packages in the alternate workspace

## Lessons Learned

On a first pass, `UMIC_TEAM4-Final` reads as a strong early systems-integration project. The repo preserves both the simulation scaffolding and the perception/control logic, which is more valuable than a polished report alone because it shows how the project was actually assembled.

The clearest second-pass opportunities are:

- a dedicated page for the `ball_detection` and perception workflow
- a dedicated page for the robot/simulation architecture across `final_description` and `final_gazebo`
- a note explaining the relationship between `src` and `src_aryan`

## Related

- [Repositories](../indexes/repositories.md)
- [Ingestion Queue](../indexes/ingestion-queue.md)

## Sources

- [Local capture](../../raw/github/umic-team4-final/2026-04-21-capture.md)
- [iamprasann/UMIC_TEAM4-Final](https://github.com/iamprasann/UMIC_TEAM4-Final)
- [UMIC_TEAM4-Final README](https://github.com/iamprasann/UMIC_TEAM4-Final/blob/master/README.md)
