import glob
import json

list_json_files = glob.glob("train/*.json")
# print(list_json_files)


conversation_count = 0
for json_file in list_json_files:
    with open (json_file,'r') as fp:
        list_dict_items = json.load(fp)

        for dict_item in list_dict_items:
            if not 'services' in dict_item:
                continue
            if 'Restaurants_1' in dict_item.get('services'):
                
                # print(dict_item.get('dialogue_id'),dict_item.get('services'))
                dialogue_id = dict_item.get('dialogue_id') 
                print(f'dialogue_id: {dialogue_id}')
                conversation_count += 1
                print(f"<<<Start: Conversation no {conversation_count}>>>")
                for turn in dict_item.get('turns'):
                    list_frames = turn.get('frames')
                    services = [frame.get('service') for frame in list_frames]
                    if not 'Restaurants_1' in services: 
                        continue
                    
                    speaker = turn.get('speaker')
                    utterance = turn.get('utterance')

                    # print(services)
                    if turn.get('speaker') == 'USER':
                        utterance = turn.get('utterance')
                        print(f'USER:{utterance}')
                    if turn.get('speaker') == 'SYSTEM':
                        utterance = turn.get('utterance')
                        print(f'SYSTEM:{utterance}')
                print(f"<<<End: Conversation no {conversation_count}>>>") 
                print('='*(len(utterance)+10))
            
            
            
        



