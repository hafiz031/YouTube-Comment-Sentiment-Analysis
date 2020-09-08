The YouTube Comment Sentiment Analysis program has the following parts:
  1. Parsing YouTube Comments
  2. Sentiment analysis

1. For Parsing YouTube comment open up the "youtube_comment_parser.py" file and before executing the code do the following:
  -> Change paste the link to the video in the `driver.get("")` line.
  -> There is also a variable called "retry", this just shows how many consecutive times the program will try to scroll comments even if it fails.
     By default I have chosen it 30, you can change it as your need. The program only parses the comments and not the replies as replies are not 
     directly related to the content of the video.
  -> After parsing is complete the program will save all the parsed comments along with commentor's name, like count and timestamp in a CSV file.

2. For sentiment analysis we need this CSV file. 
   -> Now open up the "NLP_Sentiment_Analysis_on_YouTube_Comments.ipynb" notebook and edit your project directory. 
   -> Make sure this directory contains the CSV file of parsed comments. Now enter the CSV file directory there which contains the comments.
   -> Run the notebook.
   -> Done!
   
If you are interested to know how the model was trained please go to the "training" folder and follow instruction there.
