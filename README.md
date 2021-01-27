# Real-time face recognition with audible (speech) output for Nvidia's Jetson Nano.
Following my last project, the [Food Container Identifier](https://github.com/oliver-almaraz/food_container_identifier), in which I used the Jetson Nano and the software tools provided by [dusty-nv](https://github.com/dusty-nv/jetson-inference) for making a speech descriptor of food containers, I now will use [**ageitgey's** face_recognition](https://github.com/dusty-nv/jetson-inference) Python library for doing almost tha same, but with human faces.

If you want to know more about **why it is useful**, please consult my other project's [introduction](https://github.com/oliver-almaraz/food_container_identifier/blob/main/README.md#introduction).

Also both hardware and software **requirements** are the same as my [other project's](https://github.com/oliver-almaraz/food_container_identifier/blob/main/README.md#requirements).

## Installing dependencies
Installing the dependencies is really easy, but it will take a while (more than an hour in the Jetson Nano), since some packages must be compiled from source.
*Note: I assume you already have your Jetson Nano up and running with Jetpack, and that there's a camera conected to it.

First of all, lests install the system dependencies (if you followed my food_container_identifier project, you already have `python3-pip` and `cmake` installed):

```
$ sudo apt update
$ sudo apt install python3-pip cmake libopenblas-dev liblapack-dev libjpeg-dev
```

Then the Python dependencies (will take a while):
```
sudo -H pip3 -v install Cython face_recognition opencv-python
```

## Editing the Python script
