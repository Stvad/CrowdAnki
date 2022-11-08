## General guidelines

1. When contributing to this repository, please first discuss the change you wish to make via issue, 
email, or any other method with the owners of this repository before making a change.
1. Any changes you make (unless they are very minor) should be covered by Unit tests.
1. You should test your changes by running the modified version of the plugin with your installation 
of Anki. 

## Dependencies

If you want to add new library dependency - add them to the `Pipfile`.  
The dependency management is implemented using https://pipenv.org/

## UI Files
The config window is build using QtDesigner, which you can get by running 
`sudo apt install qtcreator` 
on Linux, or simply download from `https://build-system.fman.io/qt-designer-download`

In Qt Designer you can create UI files using a simple GUI, and save them as a `.ui` file in the `ui_files` folder.

If you install the dev dependencies into your pipenv (with `pipenv install --dev`), `pyuic5` and
`pyuic6` will be available via `pipenv run pyuic5` and `pipenv run pyuic6`, respectively.
(Alternatively, you can run `pip install PyQt5 PyQt6` so that `pyuic5` and `pyuic6` are globally
available on your system.)

The `pyuic5` and `pyuic6` commands can then be used to convert the UI files to python for Qt5 and
Qt6 respectively.  See the `generate_ui.sh` script for examples.
All new UI files should be added there for automation.

This script is run automatically when packaging the extension in `package_plugin.sh`
but needs to be done manually if the UI files are changed in the dev environment.
(If you've installed `pyuic(5|6)` globally but not locally, you'll need to adjust the
`package_plugin.sh` script.)

# Testing 
## Testing your changes in Anki
 
1. If you have the production version of CrowdAnki installed - remove it from Anki. 
1. Run `fetch_dependencies.sh` - this will download the dependencies required for CrowdAnki to 
operate and put them into the `crowd_anki/dist` directory.
1. Add a symlink to the Anki plugins directory (you can find it via `Tools>Add-ons>View Files`)
pointing to `crowd_anki` directory (**you should not** name the symlink `crowd_anki` though, see 
[#62](https://github.com/Stvad/CrowdAnki/issues/62)).

At this point if you start Anki - it'd be using your development version of CrowdAnki.  
If you made some changes to the plugin while Anki is running and want to test them - you need to 
restart Anki, as plugins are loaded on Anki startup.


## Unit testing
CrowdAnki is using [Mamba](https://github.com/nestorsalceda/mamba) as a test runner. 
And it makes use of [expects](https://github.com/jaimegildesagredo/expects) assertion library.

The combination of these two tools allows you to write beautiful Spec-style tests in Python. 
 
* Install required dependencies: `pipenv install --dev`
* Running tests 
    * From CLI -  `pipenv run mamba  ./`
    * If you want to run them from IDE - do so by executing the `tests/mamba_runner.py`
* Add more to https://github.com/Stvad/CrowdAnki/tree/master/test 😉 

# Misc
## Windows development

This guide is using some shell scripts, using them is not a hard requirement, but being able to run them 
would make your life easier.  
You can achieve that in a variety of ways:
* https://docs.microsoft.com/en-us/windows/wsl/install-win10
* https://en.wikipedia.org/wiki/Cygwin 


## References
* [Anki plugin development guide](https://apps.ankiweb.net/docs/addons.html)
