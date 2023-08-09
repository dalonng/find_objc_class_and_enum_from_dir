#!/usr/bin/env python

from typing import Union
import re
import sys
import subprocess

def find_type_file_path(dir_path: str, type_str: str) -> Union[str, None]:
  command = ['fd', '--type', 'file', '--extension', 'h', f'{type_str}.h$', dir_path]
  output = subprocess.run(command, capture_output=True).stdout
  lines = output.splitlines()

  file_path = None

  files = list(filter(lambda line: '+' not in str(line), lines))
  if len(files) != 0:
    return str(files[0], 'utf-8')
    exit(0)

  # 使用 rg 查找
  command = ['rg', f'{type_str}', '-g', '*.h', dir_path]
  output = subprocess.run(command, capture_output=True).stdout
  lines = output.splitlines()

  cls_pattern = r'@interface\s+(?P<class_name>\w+)\s*:\s*(?P<superclass>\w+)\s*(<.*?>)?'

  for line in lines:
    # content = str(line).split('.h:')[1]
    match = re.search(cls_pattern, str(line))
    if match:
      class_name = match.group('class_name')
      if class_name and class_name == type_str:
        file_path = str(line, 'utf-8').split(':')[0]
        break
    # if  '@interface' in content and ':' in content:
    #   file_path = str(line, 'utf-8').split(':')[0]
    #   break
  return file_path


if __name__ == '__main__':
  n = len(sys.argv)

  if n < 2:
    print('请输入字符串')
    sys.exit(-1)

  text = sys.argv[1]
  find_type_file_path('/Users/xxx/p/xxx/xxx/xxx/', text)