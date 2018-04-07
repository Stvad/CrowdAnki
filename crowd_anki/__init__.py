try:
    # Register for https://github.com/dayjaby/AnkiHub plugin system.
    import ankihub

    ankihub.update(['Stvad/CrowdAnki'])
except:
    pass

from . import main
