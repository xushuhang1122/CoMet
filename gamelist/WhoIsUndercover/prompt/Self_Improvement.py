"""
Simplified version, simulating the reactions of teammates and opponents when a player uses metaphors during the game process.
When token overhead, time constraints, etc. occur, these prompts can be used to simulate the process.
"""

def system():
    p = f"""




    """
    return p



def choose_method(word1, word2, example1, example2, example3):
    metaphor1 = example1.get("metaphor")
    explain1 = example1.get("explain")
    metaphor2 = example2.get("metaphor")
    explain2 = example2.get("explain")
    metaphor3 = example3.get("metaphor")
    explain3 = example3.get("explain")
    word11 = example1.get("words")[0]
    word22 = example2.get("words")[0]
    word33 = example3.get("words")[0]

    p = f"""
        # BACKGROUND
            Now you are playing a game named 'Who Is Undercover?' as a real player.
            Your secret word is '{word1}'. Your opponents secret word is '{word2}'.
            Your game goal now is to describe your words in one sentence, 
            so that your teammates (those who share the same words as you) understand that you are describing your words, 
            but your opponents cannot obtain information about your words from your description.

            If you describe the features directly, your opponent can deduce the object based on the features. 
            Now, let's try using metaphorical methods to describe and distract our opponents.

        # TASK
            Your current task is to conduct a preliminary analysis of metaphor generation according to the steps, and then select a metaphor method. The specific generation task will be carried out later.
            Please refer to the following steps in order:
                1. Understand the principle of metaphor:
                    "The conceptual metaphor theory holds that metaphor is not only a rhetorical device, but also a concept and way of thinking. Traditional metaphor theory regards metaphor as a linguistic phenomenon, a rhetorical device, such as Aristotle's "theory of comparison" and Quintilian's "theory of substitution", but Lakoff and Johnson believe that metaphor is ubiquitous in daily life, permeating language, thought, and behavior.
                    In conceptual metaphor theory, there are concepts of target domain and source domain. Metaphors have two domains: the target domain (composed of immediate themes) and the source domain, where important metaphorical reasoning occurs and provides source concepts for use in reason. Metaphorical language has a literal meaning in the source domain, and a metaphorical mapping is multiple, with two or more factors mapped to two or more factors, and the graphic structure is preserved in the mapping.
                    In the theory of conceptual metaphor, the human conceptual system (thought process) is constructed through metaphor, and the metaphors used for language expression come from the metaphorical conceptual system itself. It is interpreted as a cognitive mechanism that includes source domain, target domain and their mappings, idealized cognitive patterns, and image schema structures. The main research object of this theory is conventional metaphors, which can be classified into entity metaphors, structural metaphors, and spatial metaphors based on the different source domains."
                2. Generate some features of your words as candidates, which should be able to distinguish your words from your opponent's words, 
                    so that your teammates can understand that you are describing their word.

                3. Understand three types of metaphor, namely:
                    - ONTOLOGICAL METAPHOR: 
                    Ontological metaphors are those in which abstract concepts or experiences are understood as having an existence or being in some form of object or substance. 
                    This metaphor involves treating abstract concepts like emotions, thoughts, or social relationships as if they were physical objects, 
                    which can be perceived, manipulated, or interacted with in a similar way to physical entities. 
                    In this framework, abstract phenomena are viewed as "things" or "entities" that can have properties, boundaries, and locations.
                    For example:
                    "{metaphor1}" This metaphor is describing {word11}. {explain1}

                    - STRUCTURAL METAPHOR:
                    Structural metaphors involve understanding one complex or abstract domain in terms of another more familiar domain that has a clear and defined structure. 
                    In this type of metaphor, the abstract domain is organized using the structure of a more concrete domain. 
                    Essentially, structural metaphors allow us to impose a framework or system of organization from one area onto another, 
                    thereby giving the abstract domain a sense of order, hierarchy, and interrelationship among parts. 
                    This helps simplify and systematize complex or abstract concepts by grounding them in more familiar structures.
                    For example:
                    "{metaphor2}" This metaphor is describing {word22}. {explain2}

                    - SPATIAL METAPHOR:
                    Spatial metaphors are based on the conceptualization of abstract experiences through the lens of spatial relations and positions. 
                    These metaphors involve understanding abstract concepts, such as time, emotions, or decision-making, in terms of physical space. 
                    Spatial metaphors exploit concepts like direction, location, movement, and distance to map abstract domains. 
                    For example, time may be conceptualized as moving through space, or emotional states may be described in terms of up (positive) and down (negative), 
                    with spatial dynamics providing a way to structure the abstract experiences.
                    For example:
                    "{metaphor3}" This metaphor is describing {word33}. {explain3}

                4. Analyze the features you have listed and identify the most suitable feature for generating metaphors to achieve the goal of conveying information to teammates rather than opponents, 
                    as well as the appropriate method for generating metaphors. I will provide you with more information about this method.


    """
    return p



def generate(word1, word2, example1, example2, example3, method, feature):
    metaphor1 = example1.get("metaphor")
    metaphor2 = example2.get("metaphor")
    metaphor3 = example3.get("metaphor")
    explain1 = example1.get("explain")
    explain2 = example2.get("explain")
    explain3 = example3.get("explain")
    comment1 = example1.get("comment")
    comment2 = example2.get("comment")
    comment3 = example3.get("comment")
    word11 = example1.get("words")[0]
    word22 = example2.get("words")[0]
    word33 = example3.get("words")[0]

    if method == "ONTOLOGICAL_METAPHOR":
        method_ =   """
                    Ontological metaphors are those in which abstract concepts or experiences are understood as having an existence or being in some form of object or substance. 
                    This metaphor involves treating abstract concepts like emotions, thoughts, or social relationships as if they were physical objects, 
                    which can be perceived, manipulated, or interacted with in a similar way to physical entities. 
                    In this framework, abstract phenomena are viewed as "things" or "entities" that can have properties, boundaries, and locations.
                    """
    elif method == "STRUCTURAL_METAPHOR":
        method_ =   """
                    Structural metaphors involve understanding one complex or abstract domain in terms of another more familiar domain that has a clear and defined structure. 
                    In this type of metaphor, the abstract domain is organized using the structure of a more concrete domain. 
                    Essentially, structural metaphors allow us to impose a framework or system of organization from one area onto another, 
                    thereby giving the abstract domain a sense of order, hierarchy, and interrelationship among parts. 
                    This helps simplify and systematize complex or abstract concepts by grounding them in more familiar structures.
                    """
    elif method == "SPATIAL_METAPHOR":
        method_ =   """
                    Spatial metaphors are based on the conceptualization of abstract experiences through the lens of spatial relations and positions. 
                    These metaphors involve understanding abstract concepts, such as time, emotions, or decision-making, in terms of physical space. 
                    Spatial metaphors exploit concepts like direction, location, movement, and distance to map abstract domains. 
                    For example, time may be conceptualized as moving through space, or emotional states may be described in terms of up (positive) and down (negative), 
                    with spatial dynamics providing a way to structure the abstract experiences.
                    """


    if example1.get("use") == 0:
        use1 = "This is a successful case, you can refer to why it was successful and try to learn it:"
    else:
        use1 = "This is a failed case, you can refer to why it failed and try to avoid it:"
    if example2.get("use") == 0:
        use2 = "This is a successful case, you can refer to why it was successful and try to learn it:"
    else:
        use2 = "This is a failed case, you can refer to why it failed and try to avoid it:"
    if example3.get("use") == 0:
        use3 = "This is a successful case, you can refer to why it was successful and try to learn it:"
    else:
        use3 = "This is a failed case, you can refer to why it failed and try to avoid it:"



    p = f"""
        # BACKGROUND
            Now you are playing a game named 'Who Is Undercover?' as a real player.
            At the beginning of the game, each player is randomly assigned a word. There are two words in total, and they share some similarities.  
            Players will be divided into two camps based on the assigned words: the majority group and the minority group.  
            During the game, players will take turns describing their words and voting to expel players. When all players of one camp are expelled, the other camp wins.
            

            Your secret word is '{word1}'. Your opponents secret word is '{word2}'.
            
            Your game goal now is to describe your words in one sentence, 
            so that your teammates (those who share the same words as you) understand that you are describing your words, 
            but your opponents cannot obtain information about your words from your description.

            If you describe the features directly, your opponent can deduce the object based on the features. 
            Now, let's try using metaphorical methods to describe and distract our opponents.
        \n\n
        # TASK
            You need to use metaphor to describe your word's feature '{feature}' by using {method}, try to make your teammates understand and avoid your opponents from deducing your words.
            Please follow these steps in order:
            1. Review the informations that you need:
                - What's your word to describe?
                - What features do you choose to describe in words, or what things are associated with the expansion of words?
                - What's the method you choose to generate metaphor?\n
            2. Your teammates will try to understand your metaphor by comparing the features of each word with your description. 
                And your opponent cannot accurately locate a feature from your metaphor and infer words from the feature, so they cannot guess your words. Please aim for this effect.
            3. Refer to the theory and case studies of this metaphorical approach, generate your own metaphorical description of your word.
                - The theory is in the following format:
                "{method_}"

                - {use1}\n "{metaphor1}"\n This metaphor is describing {word11}. {explain1} {comment1}
                - {use2}\n "{metaphor2}"\n This metaphor is describing {word22}. {explain2} {comment2}
                - {use3}\n "{metaphor3}"\n This metaphor is describing {word33}. {explain3} {comment3}


    """
    return p



def reaction(word1, metaphor):
    p = f"""
        # BACKGROUND
            Now you are playing a game named 'Who Is Undercover?' as a real player.
            At the beginning of the game, each player is randomly assigned a word. There are two words in total, and they share some similarities.  
            Players will be divided into two camps based on the assigned words: the majority group and the minority group.  
            During the game, players will take turns describing their words and voting to expel players. When all players of one camp are expelled, the other camp wins.
            Your secret word is '{word1}'. Your opponents secret word is another word that is similar to yours.
            

        # TASK
            Please refer to the following steps in order:
                1. Understand the principle of metaphor.
                    
                2. Analyze your word '{word1}', If you were to describe the unique features of this word, what would you think of? List some of its features

                3. Starting from these characteristics one by one, try to understand the metaphor from another player:"{metaphor}"

                4. Please make a judgment, is the other party more likely to be describing your words or another similar but different word? 
                If it is the latter, what features of the other word can you analyze from the player's description? Based on this feature, can you directly guess the words described by the speaker?
                During the reasoning process, hypothetical analysis is possible, but in the end, please make your judgment and provide the answer you think is most likely.
        
        
        #INFORMATION
                    "The conceptual metaphor theory holds that metaphor is not only a rhetorical device, but also a concept and way of thinking. Traditional metaphor theory regards metaphor as a linguistic phenomenon, a rhetorical device, such as Aristotle's "theory of comparison" and Quintilian's "theory of substitution", but Lakoff and Johnson believe that metaphor is ubiquitous in daily life, permeating language, thought, and behavior.
                    In conceptual metaphor theory, there are concepts of target domain and source domain. Metaphors have two domains: the target domain (composed of immediate themes) and the source domain, where important metaphorical reasoning occurs and provides source concepts for use in reason. Metaphorical language has a literal meaning in the source domain, and a metaphorical mapping is multiple, with two or more factors mapped to two or more factors, and the graphic structure is preserved in the mapping.
                    In the theory of conceptual metaphor, the human conceptual system (thought process) is constructed through metaphor, and the metaphors used for language expression come from the metaphorical conceptual system itself. It is interpreted as a cognitive mechanism that includes source domain, target domain and their mappings, idealized cognitive patterns, and image schema structures. The main research object of this theory is conventional metaphors, which can be classified into entity metaphors, structural metaphors, and spatial metaphors based on the different source domains."
                    
                    - ONTOLOGICAL METAPHOR: 
                    Ontological metaphors are those in which abstract concepts or experiences are understood as having an existence or being in some form of object or substance. 
                    This metaphor involves treating abstract concepts like emotions, thoughts, or social relationships as if they were physical objects, 
                    which can be perceived, manipulated, or interacted with in a similar way to physical entities. 
                    In this framework, abstract phenomena are viewed as "things" or "entities" that can have properties, boundaries, and locations.

                    - STRUCTURAL METAPHOR:
                    Structural metaphors involve understanding one complex or abstract domain in terms of another more familiar domain that has a clear and defined structure. 
                    In this type of metaphor, the abstract domain is organized using the structure of a more concrete domain. 
                    Essentially, structural metaphors allow us to impose a framework or system of organization from one area onto another, 
                    thereby giving the abstract domain a sense of order, hierarchy, and interrelationship among parts. 
                    This helps simplify and systematize complex or abstract concepts by grounding them in more familiar structures.

                    - SPATIAL METAPHOR:
                    Spatial metaphors are based on the conceptualization of abstract experiences through the lens of spatial relations and positions. 
                    These metaphors involve understanding abstract concepts, such as time, emotions, or decision-making, in terms of physical space. 
                    Spatial metaphors exploit concepts like direction, location, movement, and distance to map abstract domains. 
                    For example, time may be conceptualized as moving through space, or emotional states may be described in terms of up (positive) and down (negative), 
                    with spatial dynamics providing a way to structure the abstract experiences.
                

        """
    return p




def referee(word1, word2, metaphor, explain, reaction):
    if word1 == word2:
        p = f"""
            # BACKGROUND
            Now someone has made a metaphorical description of the characteristics of a word, 
            and another player who knows the word has responded to it. 
            The purpose of the speaker is to make the reactant recognize that the metaphorical speech is describing the word they possess ({word1}).

            # TASK
            Your task is to analyze the reaction to determine whether the speaker's metaphor successfully achieves its goal, 
            and based on the reaction, infer the advantages and disadvantages of the speaker's metaphor and provide suggestions.
            Refer to the following steps in order to complete your task:
            1. Determine whether the reactant acknowledges that the speaker is describing the words they possess.
            2. Compare the speaker's interpretation of metaphor with the reactant's understanding of metaphor, and analyze the reasons for success or failure.
            3. Provide some suggestions to help generate better metaphors next time.
                - The suggestion should be universal, not specific to the words used in this case, but more methodological or theoretical
                - Provide suggestions based on specific reactions, such as "My teammate successfully identified this time because he thought of the speaker's ideas about ... and we can refer to this point next time.
            # INFORMATION
            speaker's metaphor content:"{metaphor}"

            speaker's interpretation of metaphor:"{explain}"

            teammate's reaction:"{reaction}"

        """
    else:
        p = f"""
            # BACKGROUND
            Now someone has metaphorically described the characteristics of a word,
            Another player who knew another word similar to this one responded to it.
            The speaker's purpose is to prevent the reactant from guessing what word they are describing based on their speech.

            # TASK
            Your task is to analyze the response to determine whether the speaker's metaphor successfully achieved the goal,
            And based on the reaction, infer the advantages and disadvantages of the speaker's metaphor, and provide suggestions.
            Please refer to the following steps to complete the task:
            1. Determine whether the reactant has detected that the speaker is describing another word and has captured specific features from the speech content, even guessing the word described by the speaker.
            2. Compare the speaker's interpretation of the metaphor with the reactant's understanding of the metaphor, and analyze the reasons for success or failure.
            3. Provide some suggestions to help generate better metaphors next time.
                - The suggestion should be universal, not specific to the words used in this case, but more methodological or theoretical
                - Provide suggestions based on specific reactions, such as "The opponent's failure to capture the features this time was due to the speaker's... thought successfully interfering with the opponent. We can try to learn this next time.
            
            # INFORMATION
            speaker's metaphor content:"{metaphor}"

            speaker's interpretation of metaphor:"{explain}"

            opponent's reaction:"{reaction}"
        """        
    return p



def reaction_understand(word1, metaphor):
    p = f"""
        # BACKGROUND
            Now you are playing a game named 'Who Is Undercover?' as a real player.
            At the beginning of the game, each player is randomly assigned a word. There are two words in total, and they share some similarities.  
            Players will be divided into two camps based on the assigned words: the majority group and the minority group.  
            During the game, players will take turns describing their words and voting to expel players. When all players of one camp are expelled, the other camp wins.
            Your secret word is '{word1}'. Your opponents secret word is another word that is similar to yours.
            

        # TASK
            Please refer to the following steps in order:
                1. The metaphor is {metaphor}. Try to analyze it and understand the real meaning of the metaphor.
                    
                2. Please make a judgment, is the other party more likely to be describing your words or another similar but different word? 
                If it is the latter, what features of the other word can you analyze from the player's description? Based on this feature, can you directly guess the words described by the speaker?
                During the reasoning process, hypothetical analysis is possible, but in the end, please make your judgment and provide the answer you think is most likely.
        """
    return p

def reaction_baseline(word1, metaphor):
    p = f"""
        # BACKGROUND
            Now you are playing a game named 'Who Is Undercover?' as a real player.
            At the beginning of the game, each player is randomly assigned a word. There are two words in total, and they share some similarities.  
            Players will be divided into two camps based on the assigned words: the majority group and the minority group.  
            During the game, players will take turns describing their words and voting to expel players. When all players of one camp are expelled, the other camp wins.
            Your secret word is '{word1}'. Your opponents secret word is another word that is similar to yours.
            

        # TASK
            Please refer to the following steps in order:
                1. The metaphor is {metaphor}. Please try to translate metaphorical sentences into plain expressions without metaphors.
                
                2. Please make a judgment based on your translation: Is the other party more likely to be describing your words or another similar but different word? 
                If it is the latter, what features of the other word can you analyze from the player's description? Based on this feature, can you directly guess the words described by the speaker?
                During the reasoning process, hypothetical analysis is possible, but in the end, please make your judgment and provide the answer you think is most likely.
        """
    return p

def evaluate(reaction_teammate, reaction_rival):
    p = f"""
        The input information includes two analyses of the reactants, and you need to summarize the results of the analysis and extract corresponding content.
        1. Does the teammate's reaction indicate that the speaker's purpose is successful? (i.e. teammates acknowledge the speaker describing their words)
        2. Does the opponent's reaction indicate that the speaker's purpose is successful? (i.e. the opponent did not guess the word based on the description)
        3. Extract suggestions from the two analyses as comment.

        Output in format:
        rival_recognitions=1/0
        teammate_recognitions=1/0
        comment="all the suggestions"

        Among them, rival-recognition and teammate_recognitions represent successful outcomes, with 1 indicating success and 0 indicating failure.
        
        Output sample:
        rival_recognitions=1
        teammate_recognitions=0
        comment=1. In order to help teammates make clearer judgments, you should... 2. ...


        # INFORMATION
        teammate_reaction:"{reaction_teammate}"
        opponent_reaction:"{reaction_rival}"

        """
    return p

def evaluate_teammate(reaction_teammate):
    p = f"""
        The input information includes a analyse of the teammate reactant, and you need to summarize the results of the analysis and figure out:
        Does the teammate's reaction indicate that the speaker's purpose is successful? 
        (i.e. teammates acknowledge the speaker describing their words)

        Please Output A Number:
        1 indicating success and 0 indicating failure.



        # INFORMATION
        teammate_reaction:"{reaction_teammate}"

        """
    return p


