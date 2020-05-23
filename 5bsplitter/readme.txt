steps to running the autosplitter succesfully:

1.  have python 3 (if you don't, do install python 3)
2.  right click on firstrun.ps1 and select "run in powershell" (this will install dependencies)
3.  configure the program
    you can open fivebsplitter.py in notepad or your favourite text editor
    edit:
        splitkey : set it to what your key for splitting in livesplit
        box should now set itself, if you enconter problems, run the debug program and check if the box drawn is inside the game window 
        
4.  run fivebsplitter.py when ready (and when bounding box is within the game window)
4.1 if the program in the shell outputs "no frame :(" over and over again that means it's working
4.2 if you want 4.1 not to happen then in fivebsplitter.py set verbose to False


        
        
    PROBABLY NO LONGER NEEDED      
        box : this will be the bounding box in which we check for the advance screen. you want it in the game window, and also not that big
            (bigger would mean the program can run slower, but too small may cause false positives)
            the 4 numbers defined are : left , upper lower, right, as can be seen in the graphic contained in boundingBox.jpg
            
            if you want to see what this bounding box will look like run fivebdebugprogram.py.
            it will grab your screen and draw the box on it and save that to an image