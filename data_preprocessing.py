import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_code import llm

def remove_surrogate_characters(text):
    return re.sub(r'[\ud800-\udfff]', '', text)
    # return text.encode('utf-16', 'surrogatepass').decode('utf-16', 'ignore')

def process_post(file_path, processed_post_file_path="Dataset/processed_posts.json"):
    enriched_posts = []
    with open(file_path, encoding='utf-8', errors='ignore') as file:
        content = file.read()
        cleaned_content = remove_surrogate_characters(content)
        posts = json.loads(cleaned_content)
        
        for post in posts:
            data = extract_data(remove_surrogate_characters(post['text']))
            post_with_data = post | data
            enriched_posts.append(post_with_data)
        
    unified_tags = get_unified_tags(enriched_posts)
    
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_post_file_path, 'w', encoding='utf-8') as output:
        json.dump(enriched_posts, output, indent=4)
            
def get_unified_tags(posts):
    unique_tags = set()

    for post in posts:
        unique_tags.update(post['tags'])
        
    unique_tags_list = ', '.join(unique_tags)

    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements.
    1. Tags are unified and merged to create a shorter list.
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search".
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation".
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Personal Development"
       Example 4: "Scam Alert", "Job Scam" etc can be mapped to "Scams". 
    2. Each tag should follow title case convention. Example: "Motivation", "Job Search" etc
    3. Output should be a JSON object. No preample.
    4. Output should have mapping of original tag and unified tag.
       Example: {{"Jobseekers": "Job Search", "Job Hunting":"Job Search", "Motivation":"Motivation"}}

    Here is the list of tags:
    {tags}
    '''
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke(input={"tags":str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs!")
    
    return res

def extract_data(post):
    template = '''
    You are given a Social Media post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English, Hindi or Hinglish (Hinglish means hindi + english). 

    Here is the actual post on which you need to perform this task:
    {post}
    '''
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    response = chain.invoke(input={'post': post})
    
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse the json!")
    
    return res
    
    
if __name__ == '__main__':
    process_post("Dataset/raw_posts.json", "Dataset/processed_posts.json")