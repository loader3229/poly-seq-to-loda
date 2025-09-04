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

def get_param(seq):
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
      seq[j] = seq[j] - result[i]*((j+1)**i)
    seq.pop()
  for i in range(0,seq_len):
    result[i] = result[i] // gcd_res
  while result[len(result)-1] == 0 and len(result) >= 2:
    result.pop()
  return [result,math.factorial(seq_len-1)//gcd_res]

def to_loda(seq,split = " ; ",max_len = 10,max_num = 10000):
  result = get_param(seq)
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
  return program+"\n"

