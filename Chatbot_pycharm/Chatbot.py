import re
from nltk.corpus import wordnet

# xây dựng danh sách các từ khoá chính cần tìm kiếm và các từ đồng nghĩa
list_words=['hello','timings']
list_syn={}
for word in list_words:
    synonyms=[]
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Xoá tất cả các ký tự đặc biệt (nếu có) từ những từ đồng nghĩa
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word]=set(synonyms)

print(list_syn)

# Xây dụng dictionary lưu trữ intent và từ khoá tìm kiếm (key words)
keywords={}
keywords_dict={}
# định nghĩa ditionary lưu trữ danh sách keywords và reglular expression tương ứng phục vụ việc tìm kiếm
#định nghĩa từ khoá thứ nhất
keywords['greet']=[]
for synonym in list(list_syn['hello']):
    keywords['greet'].append('.*\\b'+synonym+'\\b.*')

#định nghĩa từ khoá thứ hai
keywords['timings']=[]
for synonym in list(list_syn['timings']):
    keywords['timings'].append('.*\\b'+synonym+'\\b.*')

#Định nghĩa dictionary lưu trữ intent và expression tương ứng sử dụng OR (|) operator
for intent, keys in keywords.items():
    keywords_dict[intent]=re.compile('|'.join(keys))

# Định nghĩa dictionary cần thiết để lưu trữ câu trả lời theo intent
responses={
    'greet':'Hello! How can I help you?',
    'timings':'We are open from 9AM to 5PM, Monday to Friday. We are closed on weekends and public holidays.',
    'unknown':'I dont quite understand. Could you repeat that?',
}

def getAnswer(user_input):
    print("user input from web" , user_input)
    matched_intent = None
    for intent,pattern in keywords_dict.items():
        # Sử dụng regular expression để tìm kiếm keywords từ dữ liệu đầu vào
        if re.search(pattern, user_input):
            matched_intent=intent

    key='unknown'
    if matched_intent in responses:
        key = matched_intent
    # Xuất câu trả lời cho người dùng
    # print ("Rule-based chatbot: ", responses[key])
    return responses[key]
#
# print ("Chào mừng bạn đến với ngân Hàng ABC (Alway be Courious)")
# while (True):
#     # lấy dữ liệu đầu vào từ người sử dụng
#     user_input = input("Please enter your question: ").lower()
#     # xác định điều kiện dừng chatbot
#     if user_input == 'quit':
#         print ("Cảm ơn bạn đã sử dụng chương trình.")
#         break
#     # matched_intent = None
#     # for intent,pattern in keywords_dict.items():
#     #     # Sử dụng regular expression để tìm kiếm keywords từ dữ liệu đầu vào
#     #     if re.search(pattern, user_input):
#     #         matched_intent=intent
#
#     result = getAnswer(user_input)
#     print("Rule-based chatbot: ", result)
#     # key='unknown'
#     # if matched_intent in responses:
#     #     key = matched_intent
#     # # Xuất câu trả lời cho người dùng
#     # print ("Rule-based chatbot: ", responses[key])

