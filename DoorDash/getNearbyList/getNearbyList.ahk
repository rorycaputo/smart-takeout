#Include ./getNearbyList/clickPickup.ahk
#Include ./getNearbyList/clickLocationArrow.ahk

GetNearbyList()
{
    ClickPickup(2000, 3000)
    ; Sleep, 333
    ; Sleep, 1703
    ; Click, 1041, 1488 Left, Down
    ; Sleep, 79
    ; Click, 1041, 1488 Left, Up
    ; Sleep, 3000
    ClickLocationArrow(0, 3000)
    ; Click, 2502, 183 Left, Down
    ; Sleep, 31
    ; Click, 2502, 183 Left, Up
    ; Sleep, 1453
    ; Click, 1394, 1437 Left, Down
    ; Sleep, 94
    ; Click, 1394, 1437 Left, Up
    ; Sleep, 2922

    Click, 1333, 719 Left, Down
    Sleep, 94
    Click, 1333, 719 Left, Up
    Sleep, 62
    Click, 1333, 719 Left, Down
    Sleep, 78
    Click, 1333, 719 Left, Up
    Sleep, 641
    Click, 1333, 727 Left, Down
    Sleep, 62
    Click, 1333, 727 Left, Up
    Sleep, 94
    Click, 1333, 727 Left, Down
    Sleep, 78
    Click, 1333, 727 Left, Up
    Sleep, 1328
    Click, 1343, 189 Left, Down
    Sleep, 63
    Click, 1343, 189 Left, Up
    Click, 1305, 1230 Left
    MouseClickDrag, Left, 1305, 1230, 1305, 300, 20
}
