import os
import json
import re
import streamlit as st
from github import Github
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load config
with open('config.json') as f:
    config = json.load(f)

# Initialize Ollama
llm = Ollama(model="mistral", temperature=0.3)

def extract_github_info(url):
    """Handle various GitHub URL formats"""
    clean_url = url.rstrip('/')
    patterns = [
        r"github\.com/([^/]+)/([^/]+)(?:/|$)",
        r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+?)(?:\.git)?$"
    ]
    for pattern in patterns:
        match = re.search(pattern, clean_url)
        if match:
            return match.group(1), match.group(2)
    return None, None

def get_key_files(repo):
    essential_files = []
    extensions = ['.py', '.js', '.md', '.txt', '.yaml', '.yml']
    
    try:
        contents = repo.get_contents("")
        while contents and len(essential_files) < 10:
            file = contents.pop(0)
            if file.type == "dir":
                contents.extend(repo.get_contents(file.path))
            elif any(file.path.lower().endswith(ext) for ext in extensions):
                try:
                    content = file.decoded_content.decode('utf-8')[:3000]
                    essential_files.append(f"## {file.path}\n```\n{content}\n```")
                except:
                    continue
    except Exception as e:
        st.warning(f"File access issue: {str(e)}")
    
    return "\n\n".join(essential_files)

def generate_guide(repo_content, repo_url):
    prompt_template = """[INST]
    Create a step-by-step guide for local implementation:
    1. Brief project summary
    2. Setup requirements
    3. Installation steps
    4. Configuration
    5. Execution instructions
    
    Repository: {repo_url}
    Key files:
    {repo_content}
    [/INST]"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["repo_content", "repo_url"])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(repo_content=repo_content, repo_url=repo_url)

def main():
    st.set_page_config(page_title="GitHub to Local Guide", page_icon="🚀")
    st.title("GitHub Project Implementation Guide")
    
    repo_url = st.text_input("GitHub Repository URL:", 
                           placeholder="https://github.com/owner/repo",
                           value="")
    
    if st.button("Generate Guide"):
        if not repo_url:
            st.warning("Please enter a GitHub URL")
            return
            
        with st.spinner("Analyzing repository..."):
            try:
                owner, repo_name = extract_github_info(repo_url)
                if not owner or not repo_name:
                    st.error("Invalid GitHub URL. Please use format: https://github.com/owner/repo")
                    return
                
                g = Github(config.get("GITHUB_TOKEN")) if config.get("GITHUB_TOKEN") else Github()
                repo = g.get_repo(f"{owner}/{repo_name}")
                
                file_content = get_key_files(repo)
                if not file_content:
                    st.error("No processable files found")
                    return
                
                guide = generate_guide(file_content, repo_url)
                
                st.success("Guide Generated!")
                st.markdown(guide)
                st.download_button("Download Guide", guide, f"{repo_name}_guide.md")
                
            except Exception as e:
                st.error(f"Processing error: {str(e)}")

if __name__ == "__main__":
    main()