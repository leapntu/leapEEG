# Psychopy EEG
This is a repository for a Psychopy experiment involving EEG at the LEAP Lab NTU.
It is designed to serve as a base for future Psychopy projects that need to interact with EEG hardware.

To recover metadata, run the `codes.py` script. It takes two command line arguments, the first is the numerical code of the trigger, and the second is the number of times the trigger has appeared. For example, to revover the metadata connected with the 2nd occurence of trigger code 5, run `python codes.py 5 2` and it will retrun the grammaticality/language and the symbol used.
