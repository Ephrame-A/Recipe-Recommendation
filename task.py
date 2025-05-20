import os


from hyperon import *

metta=MeTTa()

with open('data.metta', 'r') as file:
    content = file.read()
    metta.run(content)
# test=metta.run('!(match &self ($x $y $z $w) ($x $y $z $w))')

metta.run('''(= (pattern $par)
(let* (
        ($val (match &self ($x $y $z $w) ($x $y $z $w)))
        ($ingredient (index-atom $val 1))
)
(if (== () (subtraction-atom $ingredient $par)) $val (empty))
))''')

check = metta.run('!(pattern (Banana Strawberries Yogurt Honey))')
print(check)
