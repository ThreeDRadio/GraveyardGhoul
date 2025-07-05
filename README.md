# Graveyard Ghoul

Graveyard Ghoul runs Three D Radio graveyard timeslots.

It provides a continuous stream of music taken from Three D's music catalogue, selected at random, but meeting Three D's play quotas.

Released under the MIT licence on the off chance someone else will find it useful.

## Usage

### Config File

The app assumes a config file in the current working directory. Copy `config.yaml.example` to `config.yaml` and fill in the config values.

### Autoplay

The Ghoul has an autoplay mode, where playback will start immediately. This is off by default, meaning the user needs to press the play button. Autoplay is set by a command line flag:

```bash
./ghoul --autoplay
```

## Compilation

### OpenSuse

Station computers use OpenSuse. Most Flutter Linux guides assume a Debian style distro such as Ubuntu, so here are detailed OpenSuse instructions.

## Dependencies

You'll need to install the following packages

```bash
zypper in git-core clang cmake ninja gtk3-devel libmpv2
```

## Install Flutter SDK

Follow the Flutter guide here:

https://docs.flutter.dev/get-started/install/linux/desktop

## Check Flutter Doctor

Verify the installation:

```bash
flutter doctor
```

Correct any errors that might come up

## Clone Git Repo

```bash
git clone https://github.com/ThreeDRadio/GraveyardGhoul.git
cd GraveyardGhoul
```

## Build

```bash
flutter build linux
```

## Option 2 - Run in dev mode

You can also just run the app:

```bash
flutter run
```

# Running Compiled Binary

Unlike Ghoul 1, which needed the Python binary and a whole heap of python packages installed, Flutter apps compile to a native binary. So you can just copy the binary to other systems.

## Runtime Dependencies

Need to install the following packages:

- gtk3
- libmpv2

## Copy the file

The output from flutter build should be a binary at ` build/linux/x64/release/bundle/ghoul`. You should be able to copy this file to where it is needed.

Ghoul2 expects a config.yaml in the current working directory.

You can then just run `./ghoul` to startup.
