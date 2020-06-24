Test Page for Stuff
*******************

# Intro 

This is where an introduction will be given

# List

Why are you even still reading this ?

* To see how it looks

* Because you're procrastinating doing your own work

* Bdcause your changing this file to actually have documentation in it instead of sarcastic lists

# Sample Code

Code :: Java

class Poem{
    public WordStore storeAdverb;
    public WordStore storeNoun;
    public WordStore storeVerb;
    public WordStore storeAdjective;


    public Poem() throws IOException{
        storeAdverb = new WordStore("adverbs.txt");
        storeNoun = new WordStore("nouns.txt");
        storeVerb = new VerbStore("verbs.txt");
        storeAdjective = new WordStore("adjectives.txt");



