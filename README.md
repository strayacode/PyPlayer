# PyPlayer

Changelog:\
03/06/2019:\
. Added functions such as play, pause, next, previous\
. Added variable which you specify the path to your music\
. Themed the UI

04/06/2019:\
. Added slider to change position in the song!\
. Made it so that if the slider position is at 100, the next song will play\
. Also made it so that when the song ends, it plays the next song\
. Added 2 labels, one for current song position and another for song length. The position label updates on change in song position\
. Fixed multiple bugs:\
    . Slider speed would move according to length of song, not from normally adding\
    . When the next or previous song was played the slider would stop moving due to the amount of pixels needed for the slider to move would round to 0. This is due to the song being longer\
    . Title and current position labels wouldn't be visible until the song was played\
    
