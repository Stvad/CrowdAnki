# CrowdAnki
[![Build Status](https://travis-ci.org/Stvad/CrowdAnki.svg?branch=master)](https://travis-ci.org/Stvad/CrowdAnki)

**CrowdAnki** is a plugin for http://ankisrs.net/ that allows users to import and export decks/notes and all relevant information in a hierarchical JSON format. The main purpose is to facilitate crowdsourcing for Anki decks and notes.

AnkiWeb link for the plugin: https://ankiweb.net/shared/info/1788670778

## How to collaborate via Github
This section illustrates collaboration workflow using [Github](http://github.com).

Suppose you have a deck named DeckX and you want to collaborate on its improvement with other people. In order to achieve this you will need to:

1. Export the DeckX. You can do that by going to Anki: File > Export > 
Export format: "CrowdAnki Json Representation". Include: DeckX.
2. Create a Github account for yourself and ask your collaborators to do the same (see: https://github.com/join).
3. Create a repository for your deck by following this guide https://guides.github.com/activities/hello-world/#repository. The name of the repository has to correspond to the name of the directory that was created during the export. In our case, it would be named DeckX.
4. Add collaborators to the repository: https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/.

### CLI workflow
#### Initiating collaboration
4. Install git on your computer.
5. Go to the directory that resulted from export.
6. Initialize repository with following commands:
    
    ```
    git init
    git remote add origin git@github.com:<username>/<repository>.git
    ```

    Where <username> is your Github username (in my case Stvad) and <repository> is the name of the repository (DeckX). So in our case the command will look like:

    ```
    git remote add origin git@github.com:Stvad/DeckX.git
    ```
7. Add the content of your directory to the repository:

    ```
    git add *
    git commit -m "initial export"
    ```
8. Upload changes you've made to the Github:

    ```
    git push origin master
    ```

#### To start working on the deck your collaborators need to:

1. Install git on their machine.
2. Clone the repository you've created:

    ```
    git clone https://github.com/Stvad/DeckX.git
    ```

3. [Import the deck](#import).

If somebody **just wants to use the deck** you've uploaded to Github - they can [import decks directly from there](#import-from-github).

#### How to upload changes

When you or one of your collaborators want to upload changes you've made to the Github, you need to:

1. Get the latest changes from the Github:
    
    ```
    git pull
    ```
2. [Import the deck](#import) to combine changes you've made with the changes other people have made.
3. Export the deck the same directory where your repository is located so that export will overwrite media directory and json file in the repository. (As an alternative you can export it elsewhere and copy json file and media directory yourself to overwrite the ones that are in repository directory.)
4. Add the changes to the repository:

    ```
    git add *
    git commit -m "new updates"
    ```
5. Upload changes you've made to the Github:

    ```
    git push origin master
    ```

If you just want to **get latest changes from other people** - you need to perform only steps 1 and 2.


## Generic collaboration workflow
The current workflow could be described as following:
* The user creates or imports an Anki deck.
* He makes some modification to it (i.e. to notes, deck settings, deck structure or note models).
* Then the user can export the deck in JSON format (accompanied by media directory with media files used in that deck) and share it with other users. For example by creating Github repository with it.
* Other people then can either modify JSON directly or import the deck to their instance of Anki and then make some modifications to it.
* Original JSON then can be updated the with the changes, these people made (merging several changes together if necessary).
* After that original user (and other people) can import updated deck to integrate these new changes into their collection.

## Export
To perform the export go to menu File>Export

Select the deck (**note**: export of "All decks" is not supported, you need to select a specific deck) and the export format "CrowdAnki JSON representation".
After pressing the Export button - select directory where the result should be stored.

## Import
To perform the import go to menu File>"CrowdAnki: Import from disk" and select the directory where the deck is stored.

## Import from Github
To get the deck from Github go to menu File>"CrowdAnki: Import from Github" and enter Github username and repository name in suggested format.

So, for example, to get my [git deck](https://github.com/Stvad/Software_Engineering__git) you would need to enter Stvad/Software_Engineering__git.

### Things to note for the Import:
* Automatic backup would be triggered prior to the import;
* If note model for the note has changed, or if note model itself changed in a way that it's not easy to update it automatically: you would be prompted with the window, that will ask you to specify correspondence between old and new model;
* If the note was moved to another deck in JSON file, on import all cards from that note (except the ones, that are in dynamic decks) will be moved to the specified deck.


## Other

This plugin works with [AnkiHub plugin](https://ankiweb.net/shared/info/116826216) ([Github](https://github.com/dayjaby/AnkiHub)) to provide you better plugin management experience. 

With AnkiHub you can install plugins directly from Github and receive updates automatically.

