; color2:=0x000000
; color1:=0xF0F0F0
; MsgBox % "DiffMax:`t" ColorDiff(color1, color2) "`nDiffTotal:`t" ColorDiff(color1, color2,1)

ColorDiff(color1, color2){
  Format:=A_FormatInteger
  SetFormat, Integer, hex
  r1:=color1>>16,  r2:=color2>>16
  g1:=color1>>8&0xFF,  g2:=color2>>8&0xFF
  b1:=color1&0xFF,  b2:=color2&0xFF
  SetFormat,Integer, % Format
  diffr:=Abs(r1 - r2),  diffg:=Abs(g1 - g2), diffb:=Abs(b1 - b2)
  return diffr+diffg+diffb
}