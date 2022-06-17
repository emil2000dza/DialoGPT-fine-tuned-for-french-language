# DialoGPT fine-tuned for french language

This is a study of the impact of different type of datasets for the fine-Tuning of DialoGPT for learning french language. The report presents the different steps taken to improve the human evaluation of trained models and their perplexity. 

## Usage of the model :

The model can directly be used from a notebook using HuggingFace libray [there](https://huggingface.co/emil2000/dialogpt-for-french-language).

Otherwise, the weights of the best model obtained can be found in the path : [DialoGPT-fine-tuned-for-french-language/Chatbot DialoGPT/Output Fillm + Livre/](https://github.com/emil2000dza/DialoGPT-fine-tuned-for-french-language/tree/main/Chatbot%20DialoGPT/Output%20Fillm%20%2B%20Livre)

## Description of the repository :

### Datasets DialoGPT :
- "Film" folder gathers the transcript of movies used to fine-tune the model. It refers to the "Movie Dataset" of the report.
- "Reddit data" folder gathers the data scraped from Reddit in June 2021.
- "forum.fr Dataset" folder contains the file "ScrappingForum.fr" which scraped messages from the french forum forum.fr, the dataset is also available but was finally not studied due to limited data.
- "DialogueAndExtractDataset.txt" contains around 500 utterances of dialogues for learning french.
- "Entretiens.txt", "Theatre.txt", "Livre.txt" respectively gathers conversations extracted from interviews, theater plays and books. 
- "EthicalQuestions.txt" gathers sensible questions for which the chatbot must be prepared. 
- "EnglishCommonWords.txt" and "list-of-french-swear-words_comma-separated-text-file.txt"  are used to filter out inappropriate reddit messages for the Reddit dataset. 

### Chatbot DialoGPT :

- "Extracts from Human Evaluations"  gathers screenshots of conversations between the chatbot and the evaluators.
- "Output Film + Livre" is the folder which contains the weight of MBI dataset model.
- "GUIStreamlit.py" consists of a user interface made with the Streamlit library. 
- "Pre-Processing.ipynb" describes the pre-processing of each dataset (especially the Reddit Dataset) and perform the training of the model.
- "RedditScrapping.py" perfoms the scraping of Reddit data. 
