'''
    # print(list_json_files)
    # restaurant_tags = ['Restaurants_1','Restaurants_2']
    # hotel_tags = [] #['Hotels_1','Hotels_2','Hotels_3','Hotels_4']
'''

import glob
import json
import os
import csv


def is_service_in_scope(services,service_tags):
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

def is_service_call(calls,intended_call_method):
    if not calls:
        return False
    for call in calls:
        if not call: continue
        method = call.get('method')

        if  method and method == intended_call_method:
            return True
        
    return False

def process_files(folder,list_json_files,target_intent_domain):
    
    file_name = folder+'_'+target_intent_domain+'.csv'
    service_tags=[]
    if 'Restaurant' in target_intent_domain:
        service_tags = ['Restaurants']
    elif 'Hotel' in target_intent_domain:
        service_tags = ['Hotels']
    else:
        print("***Error: Unknown service tags. Please specify Hotels or Restaurant")


    with open (file_name,'w') as file:
        headers = ['dialogue_id' ,'conversation','services','intent','service_calls']
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        conversation_count = 0
        for json_file in list_json_files:
            with open (json_file,'r') as fp:
                list_dict_items = json.load(fp)

                for dict_item in list_dict_items:
                    if not 'services' in dict_item:
                        continue
                    # if conversation_count > 0: break
                    
                    if not is_service_in_scope(dict_item.get('services'),service_tags):
                        continue
                
                            
                    # print(dict_item.get('dialogue_id'),dict_item.get('services'))
                    dialogue_id = dict_item.get('dialogue_id') 
                    method = dict_item.get('method') 
                    # print(f'dialogue_id: {dialogue_id} , method: {method}')
                    
                    conversation = ""
                    
                    
                    # print(conversation)
                    # turns is a list and each element in list is one sentence in the converastion.
                    intents = []
                    service_call_made = False
                    for turn in dict_item.get('turns'):
                        
                        list_frames = turn.get('frames') or []
                        services = [frame.get('service') for frame in list_frames] or []
                        ''' Sometimes there are more than one service is asked in a conversation. Dialogue 80_00003 seeks
                        rideshare , mediccal practitionar, and restaurant asll.
                        '''
                        if not service_tags[0] in services[0]: continue
                        if service_call_made : continue
                        
                        intent = [is_intent(frame.get('actions')) for frame in list_frames if is_intent(frame.get('actions'))] 
                        service_calls = [frame.get('service_call') for frame in list_frames]
                        
                        if service_calls and is_service_call(service_calls,target_intent_domain) : 
                            service_call_made = True
                            conversation = conversation +  str(service_calls)  + '\n'
                            continue
                        
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
                    
                    # print(end_str)
                    
                    if target_intent_domain in intents:
                        if conversation_count >50: break
                        conversation_count += 1
                        # start_str = f"<<<Start: Conversation no {conversation_count} dialogue id {dialogue_id}>>>"
                        # end_str = f"<<<End: Conversation no {conversation_count}>>>"
                        # file.write(start_str + '\n' + conversation + end_str + '\n')
                        # # print(conversation)
                        # file.write(f"services: {services} \n")
                        # file.write(f"intent: {list(set(intents))} \n") 
                        # file.write('='*(len(utterance)+10))
                        # file.write('\n\n')
                        
                        temp_dict = {
                            'dialogue_id' : dialogue_id,
                            'conversation' : conversation,
                            'services':services,
                            'intent':list(set(intents)),
                            'service_calls':service_calls
                        }
                        writer.writerow(temp_dict)

    if os.path.exists(file_name):
        print(f"Written {file_name}")            


if __name__ == '__main__':
    #======================================================================
    target_intent_domains = ['FindRestaurants','ReserveRestaurant','SearchHotel','ReserveHotel']
    folder = 'train'
    list_json_files = glob.glob(folder + "/*.json")
    
    for target_intent_domain in target_intent_domains:
        process_files(folder,list_json_files,target_intent_domain)
    #=======================================================================
        
        
                        
                    

                
                
            



