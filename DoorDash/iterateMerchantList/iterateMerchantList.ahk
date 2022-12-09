#Include ./iterateMerchantList/init.ahk
#Include ./iterateMerchantList/goToStore.ahk
#Include ./iterateMerchant/iterateMerchant.ahk

IterateMerchantList()
{
    Init(500)
    GoToStore(0, 2000, true)
    ; Iterate store data
    IterateMerchant()


    ; while
    Click, 71, 92 Left, Down
    Sleep, 94
    Click, 71, 92 Left, Up
    Sleep, 703
    GoToStore(0, 3000)
    ; Iterate store data

    ; Todo delete
    Click, 71, 92 Left, Down
    Sleep, 94
    Click, 71, 92 Left, Up
}
