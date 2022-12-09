#Include ./iterateMerchant/initMerchant.ahk
#Include ./iterateMerchant/isBottom.ahk
#Include ../Capture2Text/captureAtCoords.ahk

IterateMerchant()
{
    InitMerchant(100, 3000)

    ; todo get top few items
    Send, {Down}
    Send, {Down}
    Send, {Down}
    Sleep, 1000

    CaptureAtCoords(1, 185, 2402, 1508)

    ; while not isBottom()
    ; {
    ;     ; add item
    ;     OutputDebug,Sending Down
    ;     Send, {Down}
    ;     Sleep, 500
    ; }



    ; ; Click, 2340, 1256
    ; Sleep, 2000
    ; ; Click, 2372, 1256
    ; OutputDebug,%color2%
    ; Sleep, 2000
    ; PixelGetColor, color3, 2372, 1268
    ; ; Click, 2372, 1268
    ; OutputDebug,%color3%
    ; Sleep, 2000
}
