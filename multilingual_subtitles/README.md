## Multilingual subtitles 

In many cases it can happen that one speaker is speaking in one language and one in another. It is very common in India that people mix Hindi and English a lot while speaking. Here we have an approach that can be used in the case where two languages are English and Hindi: 

* Find out voiced chunks from the audio using voice activity detection. 
* Generate subtitles for each voiced chunk using both English and Hindi model. 
* Here we assume a single voiced chunk contains only one language. 
* Now for each voiced chunk we have to make a choice of chosing one language over another. 
* To choose this we use KenLM based lanuage models. 
* The more probable a sentence is in a particular language, lesser the perplexity when we use that language's language model. 
* For eg. Perplexity(the weather is nice today) < P(aaj mausam accha hai) when using an English language model. 'Aaj mausam acha hai' should have been instead written in Hindi. 
* After becnhmarking our Hindi language model for baselines we see that any sentence having less than 1000 perplexity is most probably in Hindi. 
* For rest we calculate the length of the sentence and chose the output which is of greater length. 