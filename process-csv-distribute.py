# Sorry for the bad naming...
import csv, json, re

# Rely on the meta file for now
doc_meta = json.load(open('../data/metadata.json'))

# files = ['../kbdata/gene_mentions.csv', '../kbdata/phenotype_mentions.csv', '../kbdata/gene_phenotype_relation.csv']
files = ['./gene_mentions-precision/input_.csv', './phenotype_mentions-precision/input_.csv', './gene_phenotype_relation-precision/input_.csv']

'''
CONVENTION:
Save files to *.labeling.csv. e.g. for 
  ./gene_mentions-precision/input_.csv,
save output for each document to 
  ../data/PATH/TO/DOC/gene_mentions-precision.labeling.csv
'''


def DocumentExist(doc_id):
  return doc_id in doc_meta

'''
Sample data:
  journal.pone.0067134.pdf
Sample non-plos data:
  MENTION_GENE_SCPDFS_41906.pdf_372_22_22
  MENTION_GENE_SUP_long_journal.pone.0071006.pdf_50_4_5
'''    
def parseDocIdFromCsv(doc_id):
  if not doc_id.startswith('journal.') and doc_id.endswith('.pdf'):
    return False
  # assert doc_id.startswith('journal.') and doc_id.endswith('.pdf')
  return doc_id[len('journal.'):-len('.pdf')]

'''
Sample data:
  MENTION_GENE_journal.pone.0067134.pdf_571_0_0,571,
  MENTION_HPOTERM_journal.pone.0019831.pdf_249_41_42,249
'''
def parseDocIdFromMentionIdCsv(mention_id):
  if mention_id.startswith('MENTION_GENE_'):
    mention_id = mention_id[len('MENTION_GENE_'):]
  elif mention_id.startswith('MENTION_HPOTERM_'):
    mention_id = mention_id[len('MENTION_HPOTERM_'):]
  mention_id = mention_id.split('_')[0]
  return parseDocIdFromCsv(mention_id)

def getOutputDir(base_dir, doc_id):
  ''' 
  Sample data:
    base_dir: ../data/
    doc_id: pbio.1234567
  '''
  parts = doc_id.split('.')
  return '/'.join([base_dir, parts[0], parts[1][:4], parts[1][4:]]) + '/'


for f in files:
  # Save data for this csv file
  data = {}
  # kbname = f.split('/')[-1].split('.')[0]
  kbname = f.split('/')[1]
  print 'Processing', kbname
  fin = open(f)

  csv_reader = csv.reader(fin)
  header = csv_reader.next()
  attr_index = {}
  doc_id_idx = -1
  mention_id_idx = -1

  # Save all fields
  for i, h in enumerate(header):
    # determine what fields to save in index
    if h == 'mention_id':
      mention_id_idx = i
    if h == 'doc_id':
      doc_id_idx = i

  for row in csv_reader:

    try:
      if doc_id_idx == -1: 
        
        # No docid, parse docid from mentionid
        doc_id = parseDocIdFromMentionIdCsv(row[mention_id_idx])
        if doc_id == False:
          # Not a PLoS paper
          continue
      else:
        doc_id = parseDocIdFromCsv(row[doc_id_idx])
        if doc_id == False:
          continue

    except Exception as e:
      print row
      raise e

    if not DocumentExist(doc_id):
      continue

    js = {}
    for attr in attr_index:
      idx = attr_index[attr]
      field = row[idx]
      # parse bounding boxes into array
      if attr.endswith('bounding_boxes'): 
        field = parseBoundingBox(field)

      js[attr] = field

    # Save data
    if doc_id not in data:
      data[doc_id] = []

    # Save the whole csv row
    data[doc_id].append(row)

    # # DEBUG
    # break

  fin.close()

  # Dump JSON mentions
  print 'Dumping %d CSV files...' % len(data)
  for doc_id in data:
    outputdir = getOutputDir('../data', doc_id)
    savepath = outputdir + kbname + '.labeling.csv'
    # print savepath
    # print json.dumps(data[doc_id], indent=2)
    fout = open(savepath, 'w')
    csv_writer = csv.writer(fout)
    csv_writer.writerows( [header] + data[doc_id] )
    fout.close()

    # # DEBUG
    # break
