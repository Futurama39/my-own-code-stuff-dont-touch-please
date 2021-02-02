/*BFIDa 5b autosplitter
Pointers and program by Futurama39 
Harass me on github if things don't work and you think they're my fault*/

state("flashplayer_32_sa", "Flash 32")
{
    int levelcount: 0x0D1C290, 0x2C, 0xC, 0x4, 0x510, 0x788, 0x4, 0x5C4;
}
state("SAFlashPlayer", "Flash 8")
{
    int levelcount: 0x0D1C290, 0x2C, 0xC, 0x4, 0x510, 0x788, 0x4, 0x5C4;
}
state("5b", "speedrunpack")
{
    int levelcount: 0x0D1C290, 0x2C, 0xC, 0x4, 0x510, 0x788, 0x4, 0x5C4;
}
startup
{
    print("ASL started");
}
init
{
    print("Flash Found");
}
split
{
    if(current.levelcount != old.levelcount && current.levelcount != 0){
        return true;
    }
}
