import math
def reducer(seq):
  seq2 = seq
  seq_len = len(seq)
  seq = [0]*seq_len
  for i in range(0,seq_len):
    seq[i] = seq2[i]
  while True:
    seq_len = len(seq)
    if seq_len == 1:
      return seq[0]
    for i in range(0,seq_len-1):
      seq[i] = seq[i+1]-seq[i]
    seq.pop()

def get_param(seq,offset=1):
  seq2 = seq
  seq_len = len(seq)
  seq = [0]*seq_len
  for i in range(0,seq_len):
    seq[i] = seq2[i] * math.factorial(seq_len-1)
  result = [0]*seq_len
  gcd_res = math.factorial(seq_len-1)
  for i in range(seq_len-1,-1,-1):
    result[i] = reducer(seq) // math.factorial(i)
    gcd_res = math.gcd(gcd_res,result[i])
    for j in range(0,i):
      seq[j] = seq[j] - result[i]*((j+offset)**i)
    seq.pop()
  for i in range(0,seq_len):
    result[i] = result[i] // gcd_res
  while result[len(result)-1] == 0 and len(result) >= 2:
    result.pop()
  return [result,math.factorial(seq_len-1)//gcd_res]

def get_param_exp(seq,expbase,offset=1):
  seq2 = seq
  seq_len = len(seq)
  seq = [0]*seq_len
  for i in range(0,seq_len):
    seq[i] = seq2[i] * math.factorial(seq_len-1) * (expbase ** (seq_len-i))
  result = [0]*seq_len
  gcd_res = math.factorial(seq_len-1) * (expbase ** (seq_len+offset))
  for i in range(seq_len-1,-1,-1):
    result[i] = reducer(seq) // math.factorial(i)
    gcd_res = math.gcd(gcd_res,result[i])
    for j in range(0,i):
      seq[j] = seq[j] - result[i]*((j+offset)**i)
    seq.pop()
  for i in range(0,seq_len):
    result[i] = result[i] // gcd_res
  while result[len(result)-1] == 0 and len(result) >= 2:
    result.pop()
  return [result,(math.factorial(seq_len-1)  * (expbase ** (seq_len+offset)) )//gcd_res]

def get_param_fac(seq,facbase = 1,offset=1):
  seq2 = seq
  seq_len = len(seq)
  seq = [0]*seq_len
  for i in range(0,seq_len):
    seq[i] = seq2[i] * math.factorial(seq_len-1) * math.factorial(seq_len+offset+facbase-2) // math.factorial(i+offset+facbase-1)
  result = [0]*seq_len
  gcd_res = math.factorial(seq_len-1) * math.factorial(seq_len+offset+facbase-2)
  for i in range(seq_len-1,-1,-1):
    result[i] = reducer(seq) // math.factorial(i)
    gcd_res = math.gcd(gcd_res,result[i])
    for j in range(0,i):
      seq[j] = seq[j] - result[i]*((j+offset)**i)
    seq.pop()
  for i in range(0,seq_len):
    result[i] = result[i] // gcd_res
  while result[len(result)-1] == 0 and len(result) >= 2:
    result.pop()
  return [result,(math.factorial(seq_len-1)  * math.factorial(seq_len+offset+facbase-2) )//gcd_res]

def to_loda(seq,split = " ; ",max_len = 10,max_num = 10000,offset = 0):
  result = get_param(seq,offset)
  if len(result[0]) > max_len:
    return ""
  for i in range(0,len(result[0])):
    if result[0][i] > max_num:
      return ""
    if result[0][i] < -max_num:
      return ""
  if result[1] > max_num:
    return ""
  if result[1] < -max_num:
    return ""
  if len(result[0]) == 1:
    return "mov $0,"+str(result[0][0])+"\n"
  if len(result[0]) == 2 and result[0][0] == 0 and result[0][1] == 1:
    return "\n"
  if len(result[0]) == 2 and result[0][0] == 0:
    return "mul $0,"+str(result[0][1])+"\n"
  if len(result[0]) == 2 and result[0][1] == 1:
    return "add $0,"+str(result[0][0])+"\n"
  if len(result[0]) == 2:
    return "mul $0,"+str(result[0][1])+ split + "add $0,"+str(result[0][0])+"\n"
  program = "mov $1,$0"
  if result[0][len(result[0])-1] != 1:
    program = program + split + "mul $0,"+str(result[0][len(result[0])-1])
  if result[0][len(result[0])-2] != 0:
    program = program + split + "add $0,"+str(result[0][len(result[0])-2])
  for i in range(len(result[0])-3,-1,-1):
    program = program + split + "mul $0,$1"
    if result[0][i] != 0:
      program = program + split + "add $0,"+str(result[0][i])
  if result[1] != 1:
    program = program + split + "div $0,"+str(result[1])
  if offset != 0:
    return "#offset "+str(offset)+split+program+"\n"
  return program+"\n"


def to_loda_first(seq,split = " ; ",max_len = 10,max_num = 10000,offset = 0):
  result = get_param(seq[1:],offset+1)
  if len(result[0]) > max_len:
    return ""
  for i in range(0,len(result[0])):
    if result[0][i] > max_num:
      return ""
    if result[0][i] < -max_num:
      return ""
  if result[1] > max_num:
    return ""
  if result[1] < -max_num:
    return ""
  if len(result[0]) == 1:
    return "mov $0,"+str(result[0][0])+"\n"
  if len(result[0]) == 2 and result[0][0] == 0 and result[0][1] == 1:
    return "\n"
  if len(result[0]) == 2 and result[0][0] == 0:
    return "mul $0,"+str(result[0][1])+"\n"
  if len(result[0]) == 2 and result[0][1] == 1:
    return "add $0,"+str(result[0][0])+"\n"
  if len(result[0]) == 2:
    return "mul $0,"+str(result[0][1])+ split + "add $0,"+str(result[0][0])+"\n"
  program = "mov $1,$0"
  if result[0][len(result[0])-1] != 1:
    program = program + split + "mul $0,"+str(result[0][len(result[0])-1])
  if result[0][len(result[0])-2] != 0:
    program = program + split + "add $0,"+str(result[0][len(result[0])-2])
  for i in range(len(result[0])-3,-1,-1):
    program = program + split + "mul $0,$1"
    if result[0][i] != 0:
      program = program + split + "add $0,"+str(result[0][i])
  if result[1] != 1:
    program = program + split + "div $0,"+str(result[1])
  res = 0
  for i in range(1,len(result[0])):
    res += (result[0][i] * (offset**i))
  res += result[0][0]
  if res // result[1] != seq[0]:
    program = program + split + "equ $1,"+str(offset)
    mult = seq[0] - (res // result[1])
    if mult != 1 and mult != -1:
      program = program + split + "mul $1,"+str(mult)
    if mult == -1:
      program = program + split + "sub $0,$1"
    else:
      program = program + split + "add $0,$1"
  if offset != 0:
    return "#offset "+str(offset)+split+program+"\n"
  return program+"\n"


def to_loda_first_exp(seq,expbase,split = " ; ",max_len = 10,max_num = 10000,offset = 0):
  if offset < 0:
    offset = 0
  if offset > 100:
    offset = 0
  result = get_param_exp(seq[1:],expbase,offset+1)
  if len(result[0]) > max_len:
    return ""
  for i in range(0,len(result[0])):
    if result[0][i] > max_num:
      return ""
    if result[0][i] < -max_num:
      return ""
  if result[1] > max_num:
    return ""
  if result[1] < -max_num:
    return ""
  if len(result[0]) == 1:
    return ""
  program = "mov $2,"+str(expbase)+split+"pow $2,$0"+split+"mov $1,$0"
  if result[0][len(result[0])-1] != 1:
    program = program + split + "mul $0,"+str(result[0][len(result[0])-1])
  if result[0][len(result[0])-2] != 0:
    program = program + split + "add $0,"+str(result[0][len(result[0])-2])
  for i in range(len(result[0])-3,-1,-1):
    program = program + split + "mul $0,$1"
    if result[0][i] != 0:
      program = program + split + "add $0,"+str(result[0][i])
  program = program + split + "mul $0,$2"
  if result[1] != 1:
    program = program + split + "div $0,"+str(result[1])
  res = 0
  for i in range(1,len(result[0])):
    res += (result[0][i] * (offset**i))
  res += result[0][0]
  res *= (expbase**offset)
  if res // result[1] != seq[0]:
    program = program + split + "equ $1,"+str(offset)
    mult = seq[0] - (res // result[1])
    if mult != 1 and mult != -1:
      program = program + split + "mul $1,"+str(mult)
    if mult == -1:
      program = program + split + "sub $0,$1"
    else:
      program = program + split + "add $0,$1"
  if offset != 0:
    return "#offset "+str(offset)+split+program+"\n"
  return program+"\n"


def to_loda_first_fac(seq,facbase = 1,split = " ; ",max_len = 10,max_num = 10000,offset = 0):
  if offset < 0:
    offset = 0
  if offset > 100:
    offset = 0
  if facbase < 1:
    facbase = 1
  result = get_param_fac(seq[1:],facbase,offset+1)
  if len(result[0]) > max_len:
    return ""
  for i in range(0,len(result[0])):
    if result[0][i] > max_num:
      return ""
    if result[0][i] < -max_num:
      return ""
  if result[1] > max_num:
    return ""
  if result[1] < -max_num:
    return ""
  if len(result[0]) == 1:
    return ""
  program = "mov $2,"+str(facbase)+split+"fac $2,$0"+split+"mov $1,$0"
  if result[0][len(result[0])-1] != 1:
    program = program + split + "mul $0,"+str(result[0][len(result[0])-1])
  if result[0][len(result[0])-2] != 0:
    program = program + split + "add $0,"+str(result[0][len(result[0])-2])
  for i in range(len(result[0])-3,-1,-1):
    program = program + split + "mul $0,$1"
    if result[0][i] != 0:
      program = program + split + "add $0,"+str(result[0][i])
  program = program + split + "mul $0,$2"
  if result[1] != 1:
    program = program + split + "div $0,"+str(result[1])
  res = 0
  for i in range(1,len(result[0])):
    res += (result[0][i] * (offset**i))
  res += result[0][0]
  res *= math.factorial(offset)
  if res // result[1] != seq[0]:
    program = program + split + "equ $1,"+str(offset)
    mult = seq[0] - (res // result[1])
    if mult != 1 and mult != -1:
      program = program + split + "mul $1,"+str(mult)
    if mult == -1:
      program = program + split + "sub $0,$1"
    else:
      program = program + split + "add $0,$1"
  if offset != 0:
    return "#offset "+str(offset)+split+program+"\n"
  return program+"\n"


v8 = open('v8.txt','w')
t = open('stripped').read().split('\n')[4:]
offset_raw = open('offsets').read().split('\n')
offsets = {}
for i in range(0,len(offset_raw)):
  try:
    offsets[offset_raw[i].split(':')[0]]=int(offset_raw[i].split(':')[1].split(',')[0])
  except:
    pass
s = [0]*len(t)
r = []
for i in range(0,len(t)):
  offset = 0
  try:
    offset = offsets[t[i].split(',')[0][0:7]]
  except:
    pass
  s[i]=t[i].split(',')[1:]
  if len(s[i]) > 0:
    s[i].pop()
  for j in range(0,len(s[i])):
    s[i][j]=int(s[i][j])
  if len(s[i]) >= 11:
    q = to_loda_first(s[i],max_len = (len(s[i])-1)*7/10,max_num = 1e200,offset = offset)
    if q != '':
      v8.write(q)
      v8.flush()
v8.close()
