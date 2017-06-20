import json

#global variables
user_gcard = ""
user_compnents = ""

def gen_gcard(ec, ed, ao, gl):

    import uuid

    global user_gcard

    user_gcard = str(uuid.uuid4()) + ".gcard"

    with open('/home/smarky/active_dev/components/' + ec + '_components.json') as data_file:
        sam_json = json.load(data_file)

    string_sam = str(sam_json)

    with open(user_gcard, 'a') as the_file:
        if ao == "":
            for e in ed:
                the_file.write(sam_json[str(e)] + '\n')
                the_file.write(ed + '\n')
                the_file.write("-INPUT_GEN_FILE='LUND," + gl + "'")
                the_file.write("<option name= + INPUT_GEN_FILE' value='lund, filename'/>" + '\n')
        else:
            used_list = []
            for e in ed:
                if str(e) in ao:
                    used_list.append(e)
            for y in used_list:
                the_file.write(sam_json[y] + '\n')
                the_file.write(ed + '\n')
                the_file.write("-INPUT_GEN_FILE='LUND," + gl + "'")
                the_file.write("<option name= + INPUT_GEN_FILE' value='lund, filename'/>" + '\n')




