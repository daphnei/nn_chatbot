# Introduction
We chose to work with the Twitter dataset. We divided the dataset into 370000 question-answer pairs for training and 7625 question-answer pairs for validation.

# Evaluation
We trained our network to an overall perplexity of 1.78, which took 113,800 iterations.  However, during evaluation we generally prefered the output of a model that was only trained for 112,400 iterations. The results for both models on the same queries are shown below.

We evaluted the quality of each model qualitiatively by conversing with it. In our first experiment, we test the model's response to a variety of concepts that appear in the training set, or relate to culture of current events. In the second, we seed the mdoel with a random tweet from the validation set, and then pass each subsequent output tweet back into the model as input.

In both cases, we are looking for lengthy, grammatically correct, and plausible responses. In the second test, we are looking for how long the model can go without getting stuck in a loop. 

## EXPERIMENT 1 - less trained model


<pre>
> hey 
    hey buddy
> what's up <
    the best decision
> do you like my new dress?
    i don't know that anyone cares
> i care :(
    sorry adorable
> what do you think of the election results?
    why not ?
> trump
    this is the worst
> hillary
    why is this true ?
> i will make america great again
    make america great brother
> stronger together
    fuckin sexy
> what you doing this friday?
    visiting n & e
> i don't know those guys
    i'm so happy
> what are you so happy about?
    now , what are you referring to the district ?
> district nine
    she is beautiful
> you talking about the actor from hunger games?
    naturally . did i miss the other dumb ?
> dumb what?
    speech blocked
> good night
    morning dreams
<\pre>
EXPERIMENT 1 - more trained model
<pre>
> hey
    whhey , thanks
> what's up
    the best part
> do you like my new dress?
    pick new mind ... and one
> i care :(
    same then
> what do you think of the election results?
    what really mean ?
> trump
    this is real
> hillary
    trump is smart .
> i will make america great again
    make america great again
> stronger together
    youre precious
> what you doing this friday?
    come cuddle !
> i don't know those guys
    one way to find out
> what are you so happy about?
    now , what a wonderful ass \_UNK
> district nine
    she is beautiful
>  you talking about the actor from hunger games?
    likely of lack of story
> dumb what?
    \_UNK \_UNK question
> good night
    night day
</pre>

## EXPERIMENT 2 - less trained model
<pre>
> hi, thanks for your feedback. yes, i have a product hunt invite.
> keep back to you back to the dm .
> you gotta fire . keep up brotha
> keep it bro \_UNK
> thanks bro
> happiest of you
> thanks beautiful \_UNK
> you're welcome \_UNK
> thanks doll
> cool thanks !
> you're welcome
> yes ...
> ... yes
> lol
> \_UNK ...
> \_UNK ...
</pre>

## EXPERIMENT 3 - more trained model
<pre>
\> hi, thanks for your feedback. yes, i have a product hunt invite.
\> whoa , nice to connect from you to make sure :)
\> coffee . nice . coffee ? are you there ?
\> so i'm the night ... nice coffee and coffee .
\> hah hey then me way
\> a subtweet of the band
\> movie \_UNK
\> i'm so excited
\> thanks man !
\> looking good \_UNK
\> thanks girl !
\> you're welcome gorgeous
\> you're welcome \_UNK
\> thanks \_UNK
\> welcome \_UNK
\> \_UNK \_UNK
\> \_UNK \_UNK
</pre>
# Issues with chatbot
The chatbot, as it is currently implemented, has no memory beyond the past query. This means that each response is based only on the last query, which makes it difficult to have actual conversations. The chatbot also does not randomly sample from a probability distribution when generating its response. It simply picks the most likely sequence of words, which causes the same query to always generate the exact same response. A more realistic chatbot would vary its responses to the same query.

It would be fairly straightforward to fix the second problem by introducing sampling. However, the first problem of lacking memory is impossible to fix without changing datasets, as the Twitter dataset only contains question-answer pairs. Future work could also focus on better ways to penalize the network for generating shorter responses so that conversation becomes more in depth.

Lastly, we did not do any quantitiative evaluation in order to choose the best model, but for the project we plan to do so. One evaluation approch we could take is to measure out of 100 turns, how many of them are (a) grammatically correct and (b) appropriate. We would choose as the final model the one for which the sume of these values is highest.


