import glob
import json

target_intent = 'Reserve'
target_domain = 'Hotel'

target_intent_domain = target_intent+target_domain
folder = 'train'
list_json_files = glob.glob(folder + "/*.json")
# print(list_json_files)
# restaurant_tags = ['Restaurants_1','Restaurants_2']
# hotel_tags = [] #['Hotels_1','Hotels_2','Hotels_3','Hotels_4']
service_tags = ['Hotels'] #,'Hotels']
#=======================================================================

def is_service_in_scope(services):
    for service in services:
        service_tag = service.split("_")[0]
        if service_tag in service_tags:
            return True
    return False

def is_intent(actions):
    for action in actions:
        act = action.get('act')
        if act == 'INFORM_INTENT':
            # print(action.get('values'))
            return action.get('values')
    return []


with open (folder+'_'+target_intent_domain+'.txt','w') as file:

    conversation_count = 0
    for json_file in list_json_files:
        with open (json_file,'r') as fp:
            list_dict_items = json.load(fp)

            for dict_item in list_dict_items:
                if not 'services' in dict_item:
                    continue
                # if conversation_count > 0: break
                
                if not is_service_in_scope(dict_item.get('services')):
                    continue
            
                        
                print(dict_item.get('dialogue_id'),dict_item.get('services'))
                dialogue_id = dict_item.get('dialogue_id') 
                method = dict_item.get('method') 
                print(f'dialogue_id: {dialogue_id} , method: {method}')
                
                conversation = ""
                
                
                # print(conversation)
                # turns is a list and each element in list is one sentence in the converastion.
                intents = []
                for turn in dict_item.get('turns'):
                    list_frames = turn.get('frames') or []
                    services = [frame.get('service') for frame in list_frames] or []
                    intent = [is_intent(frame.get('actions')) for frame in list_frames if is_intent(frame.get('actions'))] 
                    if intent : intents.append(intent[0][0]) 
                    # print(f"actions: {actions}") 
                    
                    speaker = turn.get('speaker')
                    utterance = turn.get('utterance')

                    
                    if turn.get('speaker') == 'USER':
                        user_utterance = f'USER:{turn.get("utterance")}'
                        # print(user_utterance)
                        conversation = conversation +  user_utterance + '\n'
                    if turn.get('speaker') == 'SYSTEM':
                        system_utterance = f'SYSTEM:{turn.get("utterance")}'
                        # print(system_utterance)
                        conversation = conversation +  system_utterance + '\n'
                end_str = f"<<<End: Conversation no {conversation_count}>>>"
                # print(end_str)
                conversation = conversation + end_str + '\n'
                if target_intent_domain in intents:
                    
                    conversation_count += 1
                    start_str = f"<<<Start: Conversation no {conversation_count}>>>"
                    file.write(start_str + '\n' + conversation)
                # print(conversation)
                print(f"services: {services}")
                print(f"intent: {list(set(intents))}") 
                print('='*(len(utterance)+10))
            
                
        
    
    
                    
                

            
            
        



