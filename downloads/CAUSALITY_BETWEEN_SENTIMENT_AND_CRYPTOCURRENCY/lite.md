CAUSALITY BETWEEN SENTIMENT AND CRYPTOCURRENCY

1.
This study is about the relationship between what people say on Twitter about cryptocurrency and the value of cryptocurrency. The researchers used a machine learning algorithm to analyze tweets and identify different narratives or topics related to cryptocurrency. They found that these narratives were often linked to changes in cryptocurrency prices. The researchers believe that understanding these narratives can help predict changes in the economy. They collected a large amount of tweets from Twitter and used various techniques to clean and analyze the data. They also used a method called sentiment analysis to determine the overall sentiment or emotion expressed in the tweets. Overall, this study shows that what people say about cryptocurrency on Twitter can have an impact on its value.

2.
In this part of the paper, the authors discuss the importance of stopwords in sentiment analysis and topic modelling. Stopwords are commonly used words like "the," "and," and "in" that do not carry much meaning and can be ignored in text analysis. The authors explain that removing stopwords can make the data more useful for analysis.

They also explain two strategies for removing stopwords. The first strategy is to add extra stopwords like pronouns and common themes that appear in every tweet, such as the word "bitcoin." The authors argue that including these stopwords can skew the sentiment score towards neutral and make it less useful for sentiment analysis.

The second strategy is to use the TF-IDF (term frequency-inverse document frequency) strategy. TF-IDF calculates the significance of a word in a collection of documents. It assigns a score to each word based on its frequency in the document and its frequency in the corpus. The authors explain that TF-IDF can help identify important words in the tweets.

The authors also discuss the challenges of short text clustering, particularly when dealing with high-dimensional and sparse data like tweets. They mention that traditional topic modelling techniques like LDA (latent Dirichlet allocation) may not work well with short and sparse text data. Instead, they use a modified version of LDA called GSDMM (Gibbs Sampling Dirichlet Mixture Model) that performs well on short text clustering tasks.

Overall, this section explains the importance of preprocessing the data by removing stopwords and using appropriate techniques like TF-IDF and GSDMM for sentiment analysis and topic modelling.

3.
In this part of the paper, the authors discuss the GSDMM (Gibbs Sampling Dirichlet Mixture Model) algorithm, which is used for short text clustering and topic modelling. They explain the graphical model of DMM (Dirichlet Multinomial Mixture Model) and the important parameters involved, such as α, β, ϕ, and θ. These parameters determine the likelihood of a document being assigned to a cluster and the distribution of words within a cluster.

The authors also mention the results obtained from running the GSDMM algorithm on the collected and preprocessed tweets. They reveal 4-5 topics or narratives for each specific time period, and provide tables showing the most representative words for each narrative.

Next, the authors discuss the sentiment analysis of the tweets. They explain that they used a combination of traditional lexicon-based sentiment analysis and BERTweet, a transformer-based model, to calculate the sentiment scores. They describe the BERT (Bidirectional Encoder Representation from Transformers) model and its architecture. They also mention the Pysentimiento toolbox, which provides sentiment labels and scores for each tweet.

The authors provide an example tweet and its sentiment analysis output using Pysentimiento. They explain how they calculate a composite score for each tweet based on the positive, negative, and neutral sentiment scores. They also mention that they applied a square root function to the neutral score to adjust its impact on the composite score.

Finally, the authors discuss the results obtained from aggregating the sentiment scores of the tweets for each narrative class. They mention that tweets are continuous data streams and cannot be directly correlated with cryptocurrency pricing. Therefore, they aggregated the tweets of each day and calculated the sentiment score for that day.

Overall, this section explains the process of topic modelling and sentiment analysis on the collected tweets, as well as the results obtained for each narrative class and time period.

4.
In this part of the paper, the authors present the results of their analysis for different time periods, highlighting the relationship between narratives and cryptocurrency prices.

They discuss specific time periods and the corresponding narratives that emerged during those times. For example, they mention the period of Mt. Gox's issues in 2014, which led to a decline in investment sentiment and an increase in security narratives. They also mention the period when regulations were introduced in New York State, which resulted in a negative impact on investment sentiment.

The authors provide violin plots to visualize the sentiment distribution for different narratives during each time period. They show how the sentiment scores vary and how certain events or narratives affect the sentiment.

Furthermore, the authors discuss the co-movement of narratives and the log of Bitcoin prices. They show how certain narratives, such as regulation and technology, have a correlation with the price movements of cryptocurrencies.

Overall, this section presents the findings of the analysis and highlights the relationship between narratives, sentiment, and cryptocurrency prices. It demonstrates the impact of different events and narratives on market sentiment and provides insights into the dynamics of the cryptocurrency market.

Potential use cases of this analysis include understanding the impact of news and narratives on cryptocurrency prices, identifying sentiment trends in the market, and informing investment decisions based on sentiment analysis. It can also be used for studying the relationship between narratives and other financial assets or for analyzing sentiment in other domains beyond cryptocurrency.

