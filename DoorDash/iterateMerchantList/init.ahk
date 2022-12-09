Init(sleepBefore=100, sleepAfter=100)
{
    Sleep, sleepBefore
    Send, {Down}
    Sleep, 100
    Send, {Down}
    Sleep, 100
    Send, {Up}
    Sleep, sleepAfter
}
