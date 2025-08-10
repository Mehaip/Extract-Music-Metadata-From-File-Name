##  Current Tasks

- [ ] **Decide on table structure**
- [ ] **Implement tables**
- [ ] **Implement sqlite storage & queries (DjangoORM)**
- [ ] **Separate tracks, albums, artists, playlists by classes**
- [ ] **File Metadata & filename modifier**

## Next Tasks (Replace once all current tasks are done)

- [ ] **File naming format can be made by user**
- [ ] **Album track order** (using `genius.album_tracks`)
- [ ] **Add tests**
- [ ] **Test folder path variety/adaptability**
- [ ] **Add stats** (how many songs not found, what songs are not found, what are their names)
- [ ] **Summary reports**
- [ ] **Add log file**
- [ ] **Manual song naming** (worst case scenario)

## Problems (stuff idk how to solve)


## ✅ Finished

- [x] **Track - album association**
- [x] **Track - filepath association**
- [x] **Featured artists**

##  In the far future

- [ ] **Study remixes/covers**
- [ ] **Use incomplete album philosophy + "would you like to download the whole album?" feature**

## Album implementation
We will do the following:
Whether an album is in the database or not will be strictly the user's decision
When inserting the song, check if the album's song is in the database.
If it is, associate the songs album id to the album id.
If it isn't, consider the song a single. The song's album id can be either NULL or I can create a "single" album so that it can separate it from the others.

Database Implementation:
Because this script is supposed to work ONLY with audiofiles, we have to pay careful attention to the relationship between tables.
First things first, once a track is processed and found, we will create the artist (if it does not exist). It is mandatory that the track has an artist.
Then we will check if the Album of the track exists in the Albums table.
There are 3 scenarios:
1. The track's album is found therefore, we can just associate it with the song
2. The track is a single, therefore we leave the AlbumID NULL (or a "Single" album will be implemented)
3. The track is part of an album, but the album is not in the database. For this case go to Album impementation

Once the track has an associated artist and album, we can add the track object in the tasble.
order: We have track data from genius API -> we extract the artist -> we add the artist -> we extract the album -> we check the 3 scenarios -> we add track
