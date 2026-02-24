import os # Combines pieces of file paths 
import re # Regular Expressions for patterns in strings
import musicbrainzngs # For querying the MusicBrainz database for album info
from mutagen.flac import FLAC # For reading FLAC metadata
musicbrainzngs.set_useragent("AutoLib", "0.1", "brentonstevenson10@yahoo.com") # Set user agent for MusicBrainz API

# We need a function to clean up whatever string we use to search musicbrainz.
# we will use re.sub(pattern, replacement, string) to remove patterns and replace them.
# name = re.sub(r'\bFLAC\b', '', name, flags=re.IGNORECASE) means "In the string name (our function parameter), find anything matching the pattern \bFLAC\b, replace it with nothing i.e. delete it and satore the results back in name."
def sanitize_search_query(name):
    name = re.sub(r'\bFLAC\b', '', name, flags=re.IGNORECASE) # Remove "FLAC" from the name, do it case insensitively
    name = re.sub(r'\b\d{4}\b', '', name) # Remove 4 digit strings, aka years
    name = re.sub(r'[\[\]\(\)]', '', name) # Remove brackets and parantheses containing extra info
    name = name.replace ('_', ' ') # Python function to replace underscores with spaces
    return name.strip() # Strip gets rid of whitespaces at beginning and end of the string

# This function will clean up the folder name after we've retrieved info from musicbrainz
def sanitize_folder_name(name):
    name = re.sub(r'[<>:"/\\|?*]', '-', name) # Remove characters that are invalid in folder names, replace them with a dash
    return name.strip()

# Quick test block
##if __name__ == "__main__":
    ##messy = "Artist_Name-/Album_Title[FLAC] (2020)  "
    ##print(sanitize_search_query(messy))
    ##print(sanitize_folder_name(messy))

# Some observations:
    # I was questioning why the approach to this was to clean up existing folder/filenames to search musicbrainz instead of just cleaning up the folder names first. This question arose when my test function returned Album Name-Artist Name and I wanted speces where the dash was. 
    # I then wondered why we dont use a function to get the filename both how we want it in the directory as well as how musicbrainz can search for it. But the answer lies in the fact that albums I pull in can have wildly unpredictable folder names.
    # Making these folder names proper can be overly difficult and prone to errors. However, musicbrainz doesnt need perfection unlike my directory. And when musicbrainz uses the imperfect result of sanitize_search_query to get me an actual result, making a perfect folder name is easier.
    # So sanitize_search_query is to turn our folder name and potentially our file names into something usable to a musicbrainz search query to retrieve a resulting album. sanitize_album_name has one job AFTER the musicbrainz search. We will have a function that structures the albums folder name how we want it, but then sanitize_folder_name 's job is to remove illegal characters, giving us a final final folder name.