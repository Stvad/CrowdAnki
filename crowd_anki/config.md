## CrowdAnki

- **snapshot_path**: The path for base directory where the CrowdAnki snapshot would be written to.    
    * **Default**: `user_files` subdirectory of the extension directory.
    

- **automated_snapshot**: Whether to perform the snapshot automatically on opening/closing the application and on switching the profile.  
    * **Default**: `false` - this is an experimental feature and it's disabled by default.
    
- **snapshot_root_decks**: A list of names of the decks that should be considered `root`. 
When CrowdAnki creates a snapshot it'll create a separate git repository for each `root` deck.  
    * **Default**: Each deck with no children is considered `root`.
    * **Example**: Let's assume that you have the following decks in your collection: `a` (with sub-decks `b` and `c`), and  `d`. By default CrowdAnki is going to create 3 separate repositories - `a::b`, `a::c` and `d`.   
      If you are to add `a` to `snapshot_root_decks` then CrowdAnki would create 2 repositories instead -  `a` and `d`. The information for sub-decks `b` and `c` would be stored within repository `a` in this case. 
