import yaml
import re
import os
from Crypto.Util.number import size
stream = file('strings.yml', 'r')
document=yaml.load(stream)

entries=[]
for type in document['strings']:
    enum_entries=[]
    strings=[]

    #Enum Class (CamelCase)   
    type_class=""
    for p in re.split("_", type):
        type_class+=p.title()
        
        
    for string in document['strings'][type]:
        if(document['strings'][type][string]==None):
            enum_entries.append(type_class.upper()+"_"+re.sub("-", "_", string).upper())
        else:
            enum_entries.append(type_class.upper()+"_"+document['strings'][type][string].upper())
        strings.append(string)
        
        
    #print type
    #print type_class
    #print enum_entries
    #print strings
    
    entries.append([type, type_class, enum_entries, strings])
    

output_header="\n/*WARNING WARNING WARNING WARNING WARNING"
output_header+="\n *This file is generated by script"
output_header+="\n *generateMaps.py, to add strings change" 
output_header+="\n *strings.yml and run it again!"
output_header+="\n *WARNING WARNING WARNING WARNING WARNING\n"
output_header+=" */\n"


output_header+="#ifndef EV3STRINGS_H\n"
output_header+="#define EV3STRINGS_H\n"

output_header+=" #include <map>\n"
output_header+=" #include <string>\n"
output_header+=" using namespace std;\n\n"

output_header+="namespace ev3dev{\n"
output_header+="class Ev3Strings\n{\n"

output_header+="private: \n"
output_header+="Ev3Strings(){}/*thou shalt never construct this!*/\n"





for entry in entries:
    output_header+="public:\n"
    output_header+="\ttypedef enum\n"
    output_header+= "\t{\n"
    output_header+= "\t\t" + re.sub("-", "_", entry[1]).upper()+"_NOT_FOUND=-1,\n"
    for e in entry[2]:
        output_header+="\t\t"+ e + ",\n"
    output_header+="\t}" + entry[1] +";\n\n"
    
    output_header+="\tstatic " + entry[1] +" "+entry[1] + "FromString(const string& str);\n"
    output_header+="\tstatic string "+entry[1]+"ToString("+entry[1]+" val);\n\n"

    output_header+="\tstatic const map<"+ entry[1] +",string> " + entry[0] +"_string;\n"
    output_header+="\tstatic const map<string, "+ entry[1] +"> " + entry[0] +"_enum;\n\n"
    
    
output_header+="};\n"
output_header+="}\n"

output_header+="#endif"
output_header+="\n\n\n"



output_source="\n/*WARNING WARNING WARNING WARNING WARNING"
output_source+="\n *This file is generated by script"
output_source+="\n *generateMaps.py, to add strings change" 
output_source+="\n *strings.yml and run it again!"
output_source+="\n *WARNING WARNING WARNING WARNING WARNING\n"
output_source+=" */\n"

output_source+=" #include <ev3_driver_strings/Ev3Strings.h>\n"
output_source+="namespace ev3dev{\n"


for entry in entries:

    ##Variable Init Function Strings

    output_source+="map<Ev3Strings::"+ entry[1] +",string> init_"+ entry[0] +"_string_map()\n"
    output_source+="{\n"
    output_source+="\tmap<Ev3Strings::"+ entry[1] +",string> mp;\n"


    for e in range(len(entry[2])):
        output_source+="\tmp.insert(pair<Ev3Strings::"+ entry[1] +",string>(Ev3Strings::"+entry[2][e]+",\""+entry[3][e]+"\"));\n"


    output_source+="\treturn mp;\n"
    output_source+="}\n\n"
    
    ##Variable Init Function Enum

    output_source+="map<string, Ev3Strings::"+ entry[1] +"> init_"+ entry[0] +"_enum_map()\n"
    output_source+="{\n"
    output_source+="\tmap<string, Ev3Strings::"+ entry[1] +"> mp;\n"


    for e in range(len(entry[2])):
        output_source+="\tmp.insert(pair<string, Ev3Strings::"+ entry[1] +">(\""+entry[3][e]+"\",Ev3Strings::"+entry[2][e]+"));\n"


    output_source+="\treturn mp;\n"
    output_source+="}\n\n"
    
    output_source+="Ev3Strings::"+entry[1] +" Ev3Strings::"+entry[1] + "FromString(const string& str)\n"
    output_source+="{\n"
    output_source+="\tmap<string, Ev3Strings::"+ entry[1] +">::const_iterator it=Ev3Strings::"+ entry[0] +"_enum.find(str);\n"
    output_source+="\tif(it!=Ev3Strings::"+entry[0]+"_enum.end())\n"
    output_source+="\t{return it->second;}\n"

    output_source+="\treturn "+entry[1].upper()+"_NOT_FOUND;\n"
    output_source+="}\n\n"
    
    output_source+="string Ev3Strings::"+entry[1]+"ToString("+entry[1]+" val)\n"
    output_source+="{\n"
    output_source+="\tmap<Ev3Strings::"+ entry[1] +", string>::const_iterator it=Ev3Strings::"+ entry[0] +"_string.find(val);\n"
    output_source+="\tif(it!=Ev3Strings::"+entry[0]+"_string.end()){return it->second;}\n\n"

    output_source+="\treturn \"\";\n";
    output_source+="}\n"
    
    ##Variable

    output_source+="const map<Ev3Strings::"+ entry[1] +",string>Ev3Strings::" + entry[0] + "_string=  init_"+ entry[0] +"_string_map();\n"
    output_source+="const map<string, Ev3Strings::"+ entry[1] +">Ev3Strings::" + entry[0] + "_enum=  init_"+ entry[0] +"_enum_map();\n"

    output_source+="\n\n\n"

output_source+="}\n"


directory="../include/ev3_driver_strings/"

if not os.path.exists(directory):
    os.makedirs(directory)
    
directory="../src/ev3_driver_strings/"

if not os.path.exists(directory):
    os.makedirs(directory)
    
    

header_file = open("../include/ev3_driver_strings/Ev3Strings.h", "w")
header_file.write(output_header)
header_file.close()

source_file = open("../src/ev3_driver_strings/Ev3Strings.cpp", "w")
source_file.write(output_source)
source_file.close()
