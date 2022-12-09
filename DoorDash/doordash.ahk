#Include ../utils/activateWindow.ahk
#Include ./getNearbyList/getNearbyList.ahk
#Include ./iterateMerchantList/iterateMerchantList.ahk

start:
windowName = DoorDash ahk_class com.dd.doordash
ActivateWindow(windowName)
; GetNearbyList()
IterateMerchantList()

`::Pause


