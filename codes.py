import sys

train = """GramA X M X M
GramA V T T V T M
GramB Y Q Z P
GramB Y Z Z Q Z P
GramB W P Z Q Z P
GramA V T V T R V M
GramA V T V T M
GramA X X R T T V M
GramA V V M
GramB W W P
GramB Y Y Z W P
GramB Y Z Z Y Z W P
GramB W Q Q W P
GramA X X R V M
GramA X M M M X M
GramA X X R V T M
GramB W P Z Z Q Z P
GramB Y Z Y Z Q W P
GramA V T T V T M
GramA X X R V T M
GramA X M X M
GramB W W P
GramB Y Z Y Z Q W P
GramA X X R T T V M
GramB Y Q Z P
GramA V V M
GramA X M M M X M
GramB W Q Q W P
GramB Y Y Z W P
GramB Y Z Z Y Z W P
GramA V T V T M
GramA X X R V M
GramA V T V T R V M
GramB W P Z Q Z P
GramB Y Z Z Q Z P
GramB W P Z Z Q Z P
GramA X M M M X M
GramA X X R T T V M
GramB Y Z Z Y Z W P
GramB W W P
GramB W Q Q W P
GramB Y Y Z W P
GramA V T V T R V M
GramA X X R V M
GramA V T V T M
GramB Y Q Z P
GramB Y Z Z Q Z P
GramB W P Z Q Z P
GramA V T T V T M
GramA V V M
GramA X M X M
GramA X X R V T M
GramB Y Z Y Z Q W P
GramB W P Z Z Q Z P
GramA V T V T R V M
GramA X X R T T V M
GramA X X R V M
GramB W W P
GramB Y Z Z Q Z P
GramB Y Q Z P
GramB W P Z Z Q Z P
GramA V V M
GramA V T T V T M
GramB Y Y Z W P
GramB W P Z Q Z P
GramA X X R V T M
GramA V T V T M
GramA X M X M
GramA X M M M X M
GramB Y Z Y Z Q W P
GramB Y Z Z Y Z W P
GramB W Q Q W P
GramA V T T V T M
GramA V V M
GramB Y Z Z Q Z P
GramB Y Z Z Y Z W P
GramB W P Z Q Z P
GramB Y Z Y Z Q W P
GramA X M X M
GramA V T V T M
GramA X X R T T V M
GramB W P Z Z Q Z P
GramB W Q Q W P
GramB Y Y Z W P
GramA X X R V M
GramA V T V T R V M
GramA X X R V T M
GramA X M M M X M
GramB W W P
GramB Y Q Z P
GramA X M X M
GramA X X R T T V M
GramA V T T V T M
GramB Y Z Z Q Z P
GramB Y Q Z P
GramB W W P
GramB Y Y Z W P
GramA X X R V T M
GramA V V M
GramA V T V T R V M
GramA X M M M X M
GramB W P Z Z Q Z P
GramB W Q Q W P
GramB W P Z Q Z P
GramA X X R V M
GramA V T V T M
GramB Y Z Z Y Z W P
GramB Y Z Y Z Q W P"""

test = """GramA X M M X M	
GramA V T T V M	
GramA V T V M
GramA V V T R V M
GramA V V T M 
UngramA X M V R X M
UngramA X T X M	
UngramA V R T R M
UngramA V R V R X M
UngramA V V R T X M
GramB W P Y Z W P
GramB W Q W P
GramB W Q P Q Z P
GramB Y Y Z Q W P
GramB Y Z Q Z P	
UngramB W P P W P
UngramB Y Q Q Y P
UngramB Y Q Y P	
UngramB Y Y Q P	
UngramB Y Y Q Z Y P"""


lookup = {}
train = train.split('\n')
test = test.split('\n')

for c in xrange(21):
  lookup[c+1] = {}

i =1
for line in train:
  code = 21
  items = line.split(' ')
  category = items[0]
  for item in items[1:]: 
    lookup[code][i] = (category, item)
    i += 1

code = 1
i = 1
for line in test:
  items = line.split(' ')
  category = items[0]
  for item in items[1:]:
    lookup[code][i] = (category, item)
    i += 1
  code += 1
  i = 1

code = int(sys.argv[1])
count = int(sys.argv[2])
print(lookup[code][count])
