import os
import gzip
from tempfile import mkstemp
from shutil import move, copymode, copyfileobj

for i in range(15):
  extension = ('.' + str(i)) if i > 0 else ""
  filepath = os.path.join(os.getcwd(), "nginx_logs/access.log" + extension)

  try:
      file = open(filepath, 'r')
  except FileNotFoundError:
      filepath += '.gz'
      file = gzip.open(filepath, 'rt')

  fh, abs_path = mkstemp()
  new_file = os.fdopen(fh, 'w')

  for line in file:
    split_line = line.split(' -')
    split_line[0] = 'X.X.X.X'
    new_file.write(' -'.join(split_line))

  copymode(filepath, abs_path)
  os.remove(filepath)

  if '.gz' in filepath:
    with open(abs_path, 'rb') as f_in:
      with gzip.open(filepath, 'wb') as f_out:
        copyfileobj(f_in, f_out)
  else:
    move(abs_path, filepath)

  new_file.close()
  file.close()
