#Include ../utils/colorCompare.ahk
    
IsBottom() {
    Sleep, 250
    PixelGetColor, selected, 2392, 1256
    MouseMove, 2392, 1256
    
    PixelGetColor, unselected, 2392, 1110
    MouseMove, 2392, 1110
    Sleep, 250
    

    diff := ColorDiff(selected, unselected)
    OutputDebug,%selected%
    OutputDebug,%unselected%
    OutputDebug,%diff%

    Return diff < 30
}