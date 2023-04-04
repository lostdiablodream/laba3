import re

class rules():

    def transform(self, row):
        '''for i in self.change:
            sub_ = re.compile(i+'[0-9]+')
            row = sub_.sub(row,self.change[i])'''
        match = self.pattern.search(row)
        if match is not None:
            gd_match = match.groupdict()
            text = gd_match['text']

            replace_text = text
            for key in self.change:
                replace_text = replace_text.replace(key, self.change[key])
            numbers = self.DB.match(replace_text)
            if numbers is not None:
                dg_numbers = numbers.groupdict()
                number = int(dg_numbers['number'])
                if int(gd_match['id']) in self.range0:
                    number = number * 2 + 1
                elif int(gd_match['id']) in self.range1:
                    number = (number - 8) * 2
                new_text_numbers = dg_numbers['start'] + dg_numbers['text'] + str(number) + dg_numbers['end']
                row = match['full'].replace(text, new_text_numbers) + '\n'
        else:
            replace_text = row
            for key in self.change:

                match = re.search('(?P<start>^.*)(?P<text>' + key + ')(?P<stop>[0-9]*.*)', replace_text)
                if match is not None:
                    gd_match = match.groupdict()
                    replace_text = gd_match['start'] + gd_match['text'].replace(key, self.change[key]) + gd_match[
                        'stop']
            row = replace_text
        return row

    def __init__(self):

        self.pattern = re.compile(r'(?P<full>^.+\s+(?P<id>[0-9]+)(?P<text>\s*in\s+Word\s+\w*,\w*).+)')


        self.DB = re.compile(r'(?P<start>.*)(?P<text>DB)(?P<number>[0-9]+)(?P<end>.*)')

        self.change = {'DB': 'DB', 'DW': 'DBW', 'DD': 'DBD'}
        self.range0 = range(0, 8)
        self.range1 = range(8, 16)

class form5to7():

    def getRow(self, file_name):
        with open(file_name, 'r') as f:
            for row in f.readlines():
                yield row

    def writeFile(self, file_name):
        with open(file_name, 'w') as f:
            for row in self.result:
                f.write(row)

    def readFile(self, file_name):
        self.result.clear()
        rows = self.getRow(file_name)
        rows.send(None)
        for row in rows:
            self.result.append(self.rules.transform(row))
        return self

    def __init__(self, processing_rules=rules()):
        self.rules = processing_rules
        self.result = []

form5to7().readFile('Export.txt').writeFile('result.txt')
