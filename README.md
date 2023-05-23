## devices-simulation
# Music Player

![Device Image](./images/device.png)

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
    1. [Prerequisites](#Prerequisites)
    1. [Libraries](#Libraries)
    1. [Installation](#installation)
3. [Usage](#usage)
    1. [Remote](#Remote)
    1. [Local](#Local)
4. [Group](#Group)

## Features

- Support for multiple music formats: MP3.
- High fidelity audio playback, preserving the quality of the music.

## Getting Started

### Prerequisites

- Code **ONLY** runs on Python 3.10
- Knowlegde of using Pip
- Knowlegde of using Make

### Libraries

- pyrebase4
- python-vlc
- mutagen
- requests
- requests_toolbelt
- pylint

### Installation

1. `make venv`
#### Windows
2. enter `. .venv/Scripts/activate`
#### IOS/ Linux
2. enter `. .venv/bin/activate`
3. `make install`

## Usage

### Remote

1. `make player`
2. Control using the **Android App** or [**Website**](https://smarthome-3bb7b.web.app/)

### Local

Step 1:

2 terminals needed

terminal one `make client` <br>
terminal two `make player`

Step 2:

In terminal one -> Type commands/ actions <br>
i.e. "play", "pause", "stop", "next", "prev".

## Group

This is Group 1's simulated device.
To see all groups contributions go to the project link below! 

Project Link: https://github.com/interactive-house