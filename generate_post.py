from llm_code import llm
from few_shot_posts import FewShotPosts

fsp = FewShotPosts()

def get_length(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    else:
        return "11 to 15 lines"

def post_generator(length, language, topic):
    post_length = get_length(length)
    prompt = f'''
    Generate Social Media post using the below information. No preamble.
    
    1. Topic: {topic}
    2. Length: {post_length}
    3. Language: {language}

    If Language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be English.
    '''

    examples = fsp.get_filtered_posts(length, language, topic)
    
    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['tag']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1:
            break
        
    return prompt

if __name__ == '__main__':
    print(post_generator("Medium", "English", "Mental Health"))