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

Album implementation:
We will do the following:
Whether an album is in the database or not will be strictly the user's decision
When inserting the song, check if the album's song is in the database.
If it is, associate the songs album id to the album id.
If it isn't, consider the song a single. The song's album id can be either NULL or I can create a "single" album so that it can separate it from the others.
