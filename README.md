# CrowdAnki
[![Build Status](https://travis-ci.org/Stvad/CrowdAnki.svg?branch=master)](https://travis-ci.org/Stvad/CrowdAnki)

[[中文版介绍](README.zh_CN.md)]

**CrowdAnki** is a plugin for http://ankisrs.net/ that allows users to import and export decks/notes and all relevant information in a JSON format. The main purpose is to facilitate crowd-sourcing for Anki decks and notes.

Starting with version 0.6 it also features a close integration with Git. 
Providing you with an ability to **automatically maintain history of edits** for your decks.   
See more details [below](#snapshots). 

AnkiWeb link for the plugin: https://ankiweb.net/shared/info/1788670778

---
**Please consider supporting the plugin development by becoming a Patron - this helps me to dedicate more time and love to the project**

[![Become a Patron!](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=13102903)

---
## How to collaborate via Github
This section illustrates collaboration workflow using [Github](http://github.com).

Suppose you have a deck named DeckX and you want to collaborate on its improvement with other people. In order to achieve this you will need to:

1. Export the DeckX. You can do that by going to Anki: File > Export > 
Export format: "CrowdAnki Json Representation". Include: DeckX.
2. Create a Github account for yourself and ask your collaborators to do the same (see: https://github.com/join).
3. Create a repository for your deck by following this guide https://guides.github.com/activities/hello-world/#repository. The name of the repository has to correspond to the name of the directory that was created during the export. In our case, it would be named DeckX.
4. Add collaborators to the repository: https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/.

### GUI workflow
**Preface:**

My goal here is to provide a user-friendly description of collaboration workflow. In order to do that, I looked through multiple GUI git clients. For our purposes here, I think **Github Desktop** is the best choice (as the most user-friendly client that works). There is one problem with Github Desktop, though - it doesn't have a Linux version. Which makes me particularly sad, as I use Linux as my main OS. I've considered using Gitkraken for this tutorial, but it has some problems that disqualify it for our purposes (but if you're Linux user or if you don't like Github Desktop for some reason - you may still want to consider using it).

#### Initiating collaboration
1. Install [Github Desktop](https://desktop.github.com/) for your computer.
2. Log in to it with you Github account, created earlier.
3. Create a new repository. "Local path" should point to the place you've imported your deck, the name of the repository should be the same as the name of exported directory.
	![Image](misc/image/2.png?raw=true)
4. Add the content of your directory to the repository, by selecting all of the files, adding some comment in comment field and pressing "Commit to master"
	![Image](misc/image/4.png?raw=true)
5. Upload the changes you've just made to the Github, by pressing button "Publish" and then "Publish \<RepositoryName\>". In this case, you don't need to create repository in advance, Github Desktop will create it for you.
	![Image](misc/image/6.png?raw=true)

#### To start working on the deck your collaborators need to:
1. Install [Github Desktop](https://desktop.github.com/) for their computer.
2. Clone the repository you've created. They can do that by going to the repository page on Github and pressing "Clone or download -> Open in Desktop".
	![Image](misc/image/7.png?raw=true)
3. [Import the deck](#import).

If somebody **just wants to use the deck** you've uploaded to Github - they can [import decks directly from there](#import-from-github).

#### How to upload changes

When you or one of your collaborators want to upload changes you've made to the Github, you need to:

1. Get the latest changes from the Github, by pressing "Sync" button in the top right corner.
	![Image](misc/image/8.png?raw=true)
2. [Import the deck](#import) to combine changes you've made with the changes other people have made.
3. Export the deck the same directory where your repository is located so that export will overwrite media directory and json file in the repository. (As an alternative you can export it elsewhere and copy json file and media directory yourself to overwrite the ones that are in repository directory.)
4. Add the changes you've made to the repository, by selecting all of the files, adding some comment in comment field and pressing "Commit to master"
	![Image](misc/image/4.png?raw=true)
5. Upload changes you've made to the Github, by pressing "Sync" button in the top right corner.

If you just want to **get latest changes from other people** - you need to perform only steps 1 and 2.

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

Select the deck and the export format "CrowdAnki JSON representation".
After pressing the Export button - select directory where the result should be stored.

### Limitations:
* CrowdAnki won't allow you to do export of "All decks", you should use CrowdAnki snapshot instead.   
* Export of a filtered deck is not supported, export the main deck instead and filter it again after importing. You don't have to delete existing filtered decks, as all cards are still part of the main deck. When exporting nested decks, filtered sub-decks are just ignored.

## Import
To perform the import go to menu File>"CrowdAnki: Import from disk" and select the directory where the deck is stored.

## Import from Github
To get the deck from Github go to menu File>"CrowdAnki: Import from Github" and enter Github username and repository name in suggested format.

So, for example, to get my [git deck](https://github.com/Stvad/Software_Engineering__git) you would need to enter Stvad/Software_Engineering__git.

### Things to note for the Import:
* Automatic backup would be triggered prior to the import;
* If note model for the note has changed, or if note model itself changed in a way that it's not easy to update it automatically: you would be prompted with the window, that will ask you to specify correspondence between old and new model;
* If the note was moved to another deck in JSON file, on import all cards from that note (except the ones, that are in dynamic decks) will be moved to the specified deck.

## Snapshots

**CrowdAnki** can help you preserve **the history of edits for your decks**.  
It does this by exporting them in a specified location and creating a git commit each time you do a snapshot.

You can take snapshots manually via `File > CrowdAnki: Snapshot` menu action.  
Or you can enable automated snapshots in plugin configuration. You can find more details on how to do it [here](crowd_anki/config.md) 

Other things you can [configure](crowd_anki/config.md) is the location of the snapshot and what decks should be included into it. 
