import csv
from CTC.BlockModel import BlockModel

class LineTrackDataCSVParser:
    def __init__(self, file:str):
        self.block_list:list[BlockModel] = []
        line_name = file.split(' ')[0]

        with open(file) as track_file:
            track_reader = csv.reader(track_file, delimiter=',')
            next(track_reader)
            for row in track_reader:
                if(len(row) > 6 and row[3] != ''):
                    infrastructure:str = row[6]
                    switch_dest:list[str] = []
                    station_name:str = ""
                    railway_crossing = False

                    if(len(infrastructure) > 1):
                        # print(infrastructure)
                        infrastructure_key_words = infrastructure.split(' ', maxsplit=1)
                        if(len(infrastructure_key_words) > 1):
                            infrastructure_key_word = infrastructure_key_words[0]
                            infrasturcture_data = infrastructure.split(' ',maxsplit=1)[1]
                        else:
                            infrastructure_key_word = infrastructure_key_words[0]
                            infrasturcture_data = infrastructure_key_words[0]

                        # print(infrasturcture_data)

                        

                        if infrastructure_key_word == "STATION;":
                            try:
                                station_name = infrasturcture_data
                            except:
                                station_name = ""
                        elif infrastructure_key_word == "SWITCH":

                            switch_dest = []
                        
                            #switch is to yard
                            if infrasturcture_data.startswith("TO"):
                                switch_dest.append("YARD")
                                switch_dest.append(infrasturcture_data.split(' ')[2].lstrip('(').split('-')[0])
                            elif infrasturcture_data.startswith("FROM"):
                                switch_dest.append(infrasturcture_data.split(' ')[2].rstrip(')').split('-')[1])
                                switch_dest.append("YARD")
                            else:
                                try:
                                    switch_dest.append(infrasturcture_data.lstrip('(').rstrip(')').split('; ')[0])
                                    switch_dest.append(infrasturcture_data.lstrip('(').rstrip(')').split('; ')[1])
                                except:
                                    # print()
                                    # print(infrasturcture_data)
                                    switch_dest.append(infrasturcture_data.lstrip('(').rstrip(')').split(';')[0])
                                    switch_dest.append(infrasturcture_data.lstrip('(').rstrip(')').split(';')[1])

                        elif infrastructure_key_word == "RAILWAY":
                                railway_crossing = True

                    block = BlockModel(line=row[0], 
                                    id=row[1] + row[2],
                                    length_m=float(row[3]),
                                    speed_limit_kph=float(row[5]),
                                    station_name=station_name,
                                    switch_dest=switch_dest,
                                    railroad_crossing=railway_crossing
                                    )
                    self.block_list.append(block)
                else:
                    return
                
    def get_block_list(self):
        return self.block_list

    def print_blocks(self):
        for block in self.block_list:
            print(block)

if __name__=="__main__":
    LineTrackDataCSVParser("CTC/Green Line Track Data.csv").print_blocks()
                