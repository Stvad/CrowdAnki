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
The config window is build using QTDesigner, which you can get by running 
`sudo apt install qtcreator` 
on Linux, or simply download from `https://build-system.fman.io/qt-designer-download`

In QT Designer you can create UI files using a simple GUI, then use the `pyuic5` module to convert them to python by:

`pyuic5 ui_files/config.ui -o crowd_anki/config/config_ui.py`

This step is automatically done on packaging the extension in `package_plugin.sh`
but needs to be done manually if the UI files are changed in the dev environment.
Lastly, any new UI files should be added into the packaging script.

# Testing 
## Testing you changes in Anki
 
1. If you have the production version of CrowdAnki installed - remove it from Anki. 
1. Run `fetch_dependencies.sh` - this will download the dependencies required for CrowdAnki to 
operate and put them into the `crowd_anki/dist` directory.
1. Add a symlink to the Anki plugins directory (you can find it via `Tools>Add-ons>View Files`)
pointing to `crowd_anki` directory.

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