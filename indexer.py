import json

class Indexer:
    def __init__(self, documents:list=[]):
        self.documents = documents
        self.index = {}
        self.doc_lengths = {}
        self.total_docs = 0
    
    def index_documents(self):
        for doc in self.documents:
            doc_id = doc['doc_id']
            terms = doc['terms']
            
            self.doc_lengths[doc_id] = len(terms)
            
            for i, term in enumerate(terms):
                if term not in self.index:
                    self.index[term] = {"df": 1, "positions": {doc_id: [i]}}
                else:
                    if doc_id not in self.index[term]['positions']:
                        self.index[term]['df'] += 1
                        self.index[term]['positions'][doc_id] = [i]
                    else:
                        self.index[term]['positions'][doc_id].append(i)
        
        self.total_docs = len(self.documents)
        return self.index
    
    def save_index_json(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.index, f)
    
    def load_index_json(self, file_name):
        with open(file_name, 'r') as f:
            self.index = json.load(f)
        return self.index
    
    def save_index(self, file_name):
        with open(file_name, 'w') as f:
            for term in self.index:
                f.write(term + ':\n')
                f.write('\t\tdf: ' + str(self.index[term]['df']) + '\n')
                f.write('\t\tpositions:\n')
                for doc_id in self.index[term]['positions']:
                    positions = ",".join(map(str, self.index[term]['positions'][doc_id]))
                    f.write('\t\t\t' + str(doc_id) + ': ' + positions + '\n')
    
    def load_index(self, file_name):
        with open(file_name, 'r') as f:
            term = None
            for line in f:
                line = line.rstrip('\n')
                
                if line and not line.startswith('\t'):
                    term = line.rstrip(':')
                    self.index[term] = {"df": 0, "positions": {}}
                    
                elif line.strip().startswith('df:'):
                    self.index[term]['df'] = int(line.split('df:')[1].strip())
                    
                elif line.startswith('\t\t\t') and ':' in line:
                    doc_id, positions_str = line.strip().split(':', 1)
                    positions = [int(pos) for pos in positions_str.split(',') if pos.strip()]
                    self.index[term]['positions'][doc_id] = positions
        
        return self.index
    
    def get_term(self, term):
        return self.index[term]

    def save_doc_lengths(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.doc_lengths, f)
    
    def load_doc_lengths(self, file_name):
        with open(file_name, 'r') as f:
            self.doc_lengths = json.load(f)
        return self.doc_lengths
    
    def save_total_docs(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self.total_docs))
    
    def load_total_docs(self, file_name):
        with open(file_name, 'r') as f:
            self.total_docs = int(f.read().strip())
        return self.total_docs