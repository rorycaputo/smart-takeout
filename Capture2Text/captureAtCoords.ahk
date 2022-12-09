; start:
; CaptureAtCoords(0,0,230,30)

CaptureAtCoords(x_start, y_start, x_end, y_end)
{
    ; RunWait, C:\Users\Rory\Downloads\Capture2Text_v3.9\Capture2Text\Capture2Text.exe %x_start% %y_start% %x_end% %y_end%
    ; RunWait, C:\Program Files\Capture2Text\Capture2Text_CLI.exe %x_start% %y_start% %x_end% %y_end%  --clipboard
    RunWait, C:\Program Files\Capture2Text\Capture2Text_CLI.exe  --screen-rect "%x_start% %y_start% %x_end% %y_end%" -b  --clipboard
    MsgBox, %clipboard%
}