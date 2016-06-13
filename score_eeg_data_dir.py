import os, sys

def get_grammar(line_num):
  if line_num <= 10:
    return "A"
  else:
    return "B"

def get_grammaticality(line_num):
  if line_num in [1,2,3,4,5,11,12,13,14,15]:
    return "grammatical"
  else:
    return "ungrammatical"

def extract_data(raw_text):
  array_str = '['
  last_char = ''
  read = False
  for char in raw_text:
    if char == '[' and last_char == '[':
      read = True
      array_str += char
      continue
    if char == ']' and last_char ==  ']':
        array_str += char
        break
    if read == True:
      array_str += char
    last_char = char
  data = eval(array_str)
  return data

def read_file(path_str):
  file_obj = open(path_str)
  raw_text = file_obj.read()
  data = extract_data(raw_text)
  return data

def score_response(response):
  grammar = get_grammar(response[0])
  grammaticality = get_grammaticality(response[0])
  subject_answer = response[1]
  correct = '0'
  if grammaticality == 'grammatical' and subject_answer == 'y':
    correct = '1'
  if grammaticality == 'ungrammatical' and subject_answer == 'n':
    correct = '1'
  return [grammar, grammaticality, subject_answer, correct]

def score_responses(response_list):
  scored = []
  order = 0
  for response in response_list:
    order += 1
    scored_response = score_response(response)
    scored_response += [str(order)]
    scored += [scored_response]
  return scored

def write_output(data):
  out = open('eeg_out.csv','w')
  out.write('subject, grammar, grammaticality, subject_answer, correct, order\n')
  for subject, responses in data.items():
    print(responses)
    for response in responses:
      out_line = subject
      for datum in response:
        out_line += ', ' + datum
      out_line += '\n'
      out.write(out_line)

def score_directory(directory_str):
  file_names = os.listdir(directory_str)
  responses = []
  subjects = []
  for file_name in file_names:
    data = read_file(directory_str+file_name)
    responses += [data]
    subjects += [file_name.split("_")[0]]
  print(responses)
  scored_responses = []
  for response_list in responses:
    scored_responses += [score_responses(response_list)]
  data = {}
  for subject, scored_response in zip(subjects, scored_responses):
    data[subject] = scored_response
  return data

data_directory = sys.argv[1]
processed_data = score_directory(data_directory)
write_output(processed_data)
