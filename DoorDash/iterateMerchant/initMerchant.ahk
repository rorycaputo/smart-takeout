InitMerchant(sleepBefore=100, sleepAfter=100)
{
    Sleep, sleepBefore
    Click, 1305, 1200 Left
    MouseClickDrag, Left, 1305, 1200, 1305, 300, 20
    Send, {Up, down}
    Sleep, 2000
    Send, {Up, up}
    Send, {Down}
    Sleep, 100
    Send, {Down}
    Sleep, 100
    Send, {Down}
    Sleep, 100
    Send, {Down}
    Sleep, 100
    Send, {Tab}
    Send, {Down}
    Sleep, 100
    Send, {Down}
    Sleep, sleepAfter
}
