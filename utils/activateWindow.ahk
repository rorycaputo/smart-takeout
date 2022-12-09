ActivateWindow(windowName){
    WinWait, %windowName%, 
    IfWinNotActive, %windowName%, , WinActivate, %windowName%, 
    WinWaitActive, %windowName%, 
}