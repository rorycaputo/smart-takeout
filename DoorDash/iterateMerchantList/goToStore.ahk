GoToStore(sleepBefore=100, sleepAfter=100, isFirst=false)
{
    Sleep, sleepBefore
    if isFirst
    {
        Click, 1037, 731 Left, Down
        Sleep, 125
        Click, 1037, 731 Left, Up
    }
    else
    {       
        Click, 1037, 1243 Left, Down
        Sleep, 109
        Click, 1037, 1243 Left, Up
    }
    Sleep, sleepAfter
}
