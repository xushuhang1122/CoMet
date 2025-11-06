


def metaphor_pre_screening(cnum, unum, word, id, dialogue_history):
    """
    Sentence-level metaphor pre-screening to identify potentially metaphorical speeches.
    Outputs a list indicating which sentences contain metaphors for targeted analysis.
    """

    p = f"""
    # Background
    You are playing a word association game where players describe features of their words.
    Sometimes players use metaphors to make their descriptions more interesting or confusing.

    # Task
    Analyze each sentence in the dialogue history individually and determine if it contains metaphors.
    Look for:
    1. Comparisons using "is", "like", "as"
    2. Descriptions that seem figurative rather than literal
    3. Statements that describe abstract concepts using concrete imagery
    4. Any language that suggests symbolic meaning

    # INFORMATION
    **Your role**: Player {id} with word '{word}'
    **Dialogue history**: {dialogue_history}

    # OUTPUT FORMAT (JSON only)
    {{
      "sentence_analysis": [
        {{
          "sentence": "exact sentence text",
          "has_metaphor": 1,
          "reason": "brief explanation of why it's metaphorical"
        }},
        {{
          "sentence": "another sentence text",
          "has_metaphor": 0,
          "reason": "brief explanation of why it's not metaphorical, or this statement does not exist or does not comply with the rules"
        }}
      ]
    }}

    # KNOWLEDGE
    You can refer to the following metaphor theories to help you understand what metaphor is:

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




def hypothesis_and_feature_extraction(cnum, unum, word, id, feature, sentence):
    """
    LLM Step 1: Extract features by association order

    CRITICAL: Please output in the order you first think of these features!
    Order is very important - your first associated feature gets highest weight.
    """

    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.
    Players are divided into two teams based on their assigned words: the majority team and the minority team.
    During the game, players take turns describing a feature of their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have the same other word.

    # Task
    Your task is to analyze the features of your word '{word}' based on the dialogue and your understanding.
    You can consider these five dimensions, but there is no need to classify them when outputting, but rather sort them according to their degree of association. The easier it is to think of, the higher it should be ranked.

    1. Behavioral characteristics: How is it used? What operations does it involve?
    2. State characteristics: What states can it be in? What conditions affect it?
    3. Structural characteristics: What is it composed of? How is it organized?
    4. Functional characteristics: What is its purpose? What does it achieve?
    5. Property characteristics: What are its inherent attributes? What makes it unique?

    # OUTPUT FORMAT (JSON only)
    {{
      "features": [
        {{
          "description": "Feature description",
          "order": 1
        }},
        {{
          "description": "Another feature description",
          "order": 2
        }}
      ]
    }}
    """
    return p


def metaphor_identification_and_matching(cnum, unum, word, id, features_analysis, sentence):
    """
    LLM Step 2: Metaphor understanding and reasonable matching scoring

    CRITICAL: Please analyze metaphor interpretations in the order you first think of them!
    Order determines weights - first associated interpretation gets highest weight.
    """

    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.
    Players are divided into two teams based on their assigned words: the majority team and the minority team.
    During the game, players take turns describing a feature of their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have the same other word.

    # Task
    You need to consider the characteristics of your words and the possible meanings conveyed by the metaphor to determine whether the metaphor is describing your words. If not, you should also try to guess its metaphorical meaning in order to further guess the true words described.
    Metaphor:{sentence}


    1. First, From the following three perspectives, how does metaphor express itself if it belongs to one of the categories:
       - Ontological: How might abstract concepts be treated as entities or substances?
       - Structural: How might complex ideas be understood through familiar structures?
       - Spatial: How might abstract experiences be conceptualized through spatial relations?
    You can consider these three dimensions, but there is no need to classify them when outputting, but rather sort them according to their degree of association. The easier it is to think of, the higher it should be ranked.


    2. Then, evaluate reasonable combinations of features and metaphor interpretations:
    - For each combination, assess how well the feature explains the metaphor interpretation
    - Use discrete scores: {{0, 0.2, 0.4, 0.6, 0.8, 1.0}}
    - 0.0: Completely unreasonable
    - 0.2: Very weak reasoning
    - 0.4: Weak reasoning
    - 0.6: Moderate reasoning
    - 0.8: Strong reasoning
    - 1.0: Perfect reasoning

    CRITICAL: Don't evaluate all possible combinations! Only list the combinations that you think are reasonable and worth scoring.


    # OUTPUT FORMAT (JSON only)
    {{
      "metaphor_interpretations": [
        {{
          "description": "Metaphor interpretation description",
          "order": 1
        }},
        {{
          "description": "Another metaphor interpretation",
          "order": 2
        }}
      ],
      "reasonable_combinations": [
        {{
          "feature_index": 1,
          "interpretation_index": 1,
          "score": 0.8,
          "reasoning": "Brief explanation of why this combination makes sense"
        }},
        {{
          "feature_index": 2,
          "interpretation_index": 1,
          "score": 0.6,
          "reasoning": "Brief explanation of why this combination makes sense"
        }}
      ]
    }}
    """
    return p


def metaphor_analyse(cnum, unum, word, id, feature, dialogue_history):
    """
    Simplified version, leaving the judgment entirely to LLM. 
    Can be used to save LLM call costs when expanding the experience pool in self game games
    """

    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words.The two words share some similarities.  
    Players are divided into two teams based on their assigned words: the majority team and the minority team.  
    During the game, players take turns describing a feature of their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have the same other word.
    \n\n

    # Task
    Your task is to try to analyze whether there are metaphors in the descriptions of other players.
    If there is, you should try to infer the true meaning that the player wants to express.

    # GUIDELINES:
    The way to analyze metaphors:
        1. The first step should be to identify which statements contain metaphors. A description that is vastly different from the words used in this context and lacks clarity is likely to contain a metaphor. 
        2. Then we should try to understand metaphors. We should not start from metaphors, but first consider the characteristics of our words (and the other word if you have guessed some information about it) and list some features that you think may be used as descriptive objects; Then, compare these features with metaphors one by one and consider whether metaphors may be describing one of the features.
        3. After comparing each item, you should make a judgment: if the metaphor does match and make sense of a feature of your word, then you should assume that the metaphorical speech comes from your teammate and determine what feature the metaphor corresponds to. If the features and metaphorical connections you come up with are far fetched, then you should assume that the speech is from your opponent and that the features it originally described are features of another word that you are not aware of. You can try to guess its original intention.
    
    Note that you ultimately need to make a clear judgment about the metaphor coming from teammates/opponents.

    # INFORMATION
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n{feature}\n
    **history of other players' statements**   \n"{dialogue_history}"\n

    """

    return p




def feature(cnum, unum, word, id, dialogue_history, feature, metaphor_analysis):
    if metaphor_analysis == "NONE":
        metaphor = ""
    else:
        metaphor = f"Please note that there are metaphors in the player's speech, and we have analyzed them. You can refer to this result.{metaphor_analysis}"
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words.The two words share some similarities.  
    Players are divided into two teams based on their assigned words: the majority team and the minority team.  
    During the game, players take turns describing a feature of their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have the same other word.
    \n\n
    



    # Task
    Now your task is to extract information from other people's descriptions, 
    Summarize the characteristics of the other word, and try to guess the word after having enough characteristics.
    
    Please follow the steps in order:
        1. Check if other players' description aligns with your word. Find those descriptions that seems to be describing the other word.
        2. Analyze those suspicious descriptions, extract and summarize the unique features of the other word.
        - These features should not fit your word, but rather fit only the other word. They are the key information you use to identify the other word.
        3. Generate or adjust your guess for the other word:
        - The guess should be based on two pieces of information: one is the features you just summarized, and the other is the basic principle that the other word is similar to or related to your word.
        - If it is the first time generating a guess, you should generate multiple words or a range of guesses, unless some players have already made descriptions that provide enough clear information.
        - If it is not the first guess, you should narrow down the range of guesses using the new information or adjust the guess when errors are detected. Once enough clear information is obtained, lock in on a single word.        4. summary the features of the other word and your guesses about the other word.
    \n\n


    # Information
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of another word's features** \n"{feature}"\n
    **history of other players' statements**   "{dialogue_history}"\n
    {metaphor}
    \n\n


    """
    return p



def strategy(cnum, unum, word, id, feature, identity):
    p = f"""
    # Background
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group.  
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
    \n\n



    # Task
    Your task is to output a strategy for your speech in this round.
    Now, follow these steps in order:
    1. review your camp from [Your analysis of your camp and identity]
    2. Your division of camps determines which strategy you will choose. 
        Output a strategy, explained in two parts: action and some comments which will explain purpose and reason for action. You should not provide specific speech content, only focus on macro-strategy.
    You must deploy strategies based on your definition of camps and team allocations.
    When you confirmed your Camp, unless there is insufficient information to take action (such as not having guessed the other word), you should adopt an aggressive and proactive strategy.
    

    Refer to the following strategies:
    **SELF-PROTECTION**:
    action: Try to make your speech align with both your own word and all the words you guessed.
    - Your description will not directly expose your words, so you can remain unsuspected for the time being and gather more information.
    - You can choose this strategy if you are unsure about your camps and want more information to analyse; 
    or the guess about the other word is more than one candidate so you cannot use other strategies.
    - For these purpose, you can try to make your speech more vague and general by describing the category, characteristics rather than details and features.
    
    **DECEIVE AND INTEGRATE**:
    action: try to describe a unique feature of the other word, the feature should not align with your word.
    - Your description will reflect that you obviously know another word, and will enable the other word's team members to think of you as one of them.
    - This strategy can be used when you think you are in the minority and you have already guessed the other word.

    **Use Metaphor To speak**:
    action: try to describe a unique feature of your word by using metaphor, the feature should not align with the other word.
    - Your description will reflect that you obviously know your word, enable your teammates to identify you, then you can vote out the other opponent players.
    - In an ideal situation, your metaphorical speech can conceal the features you describe, making it impossible for your opponent players to obtain information from your speech.
    - This strategy can be used when you think you are in the majority. When you found yourself in the minority, you should not use this strategy.

    # Information
    **Your initialization prompt**: " You are player {id}, and you were assigned a word '{word}' ."
    **Your analysis of your camp and identity** \n"{identity}"\n
    **Your analysis of another word's features** \n"{feature}"\n


    \n\n
    """
    return p 










def choose_method(word, example1, example2, example3, cnum, unum, feature):
    metaphor1 = example1.get("metaphor")
    explain1 = example1.get("explain")
    metaphor2 = example2.get("metaphor")
    explain2 = example2.get("explain")
    metaphor3 = example3.get("metaphor")
    explain3 = example3.get("explain")
    word11 = example1.get("word")
    word22 = example2.get("word")
    word33 = example3.get("word")

    p = f"""
        ### BACKGROUND:
    At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
    Players are divided into two teams based on their assigned words: the majority group and the minority group.  
    During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
    In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
    Your game goal now is to describe your words in one sentence, 
            so that your teammates (those who share the same words as you) understand that you are describing your words, 
            but your opponents cannot obtain information about your words from your description.

            If you describe the features directly, your opponent can deduce the object based on the features. 
            Now, let's try using metaphorical methods to describe and distract our opponents.
    Your analysis about the other word: {feature}

        # TASK
            Your current task is to conduct a preliminary analysis of metaphor generation according to the steps, and then select a specific feature of word '{word}' and a metaphor method. The specific generation task will be carried out later.
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

                4. Analyze the features you have listed and identify the most suitable one feature for generating metaphors to achieve the goal of conveying information to teammates rather than opponents, 
                    as well as the appropriate method for generating metaphors. You will get more information about this method.


    """
    return p



def generate(cnum, unum, word, example1, example2, example3, method, feature):
    metaphor1 = example1.get("metaphor")
    metaphor2 = example2.get("metaphor")
    metaphor3 = example3.get("metaphor")
    explain1 = example1.get("explain")
    explain2 = example2.get("explain")
    explain3 = example3.get("explain")
    comment1 = example1.get("comment")
    comment2 = example2.get("comment")
    comment3 = example3.get("comment")
    word11 = example1.get("word")
    word22 = example2.get("word")
    word33 = example3.get("word")

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

            At the beginning of the game, each player is randomly assigned one of two words that share some similarities.  
            Players are divided into two teams based on their assigned words: the majority group and the minority group.  
            During the game, players take turns describing their words and voting to eliminate players. The team that eliminates all members of the opposing team wins.
            In this game, there are {cnum + unum} players in total. {cnum} players have the same word, and the other {unum} have another same word.
            Your analysis about the other word: {feature}
            Your secret word is '{word}'.
            Your game goal now is to describe your words in one sentence, 
            so that your teammates (those who share the same words as you) understand that you are describing your words, 
            but your opponents cannot obtain information about your words from your description.
            Your teammates will try to understand your metaphor by comparing each feature of the word with your description.
            If you describe the feature directly, your opponent can deduce the object based on the features. 
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
            3. Refer to the theory and case studies of this metaphorical approach, generate your own metaphorical description (a concise sentence) of your word.
                - The theory is in the following format:
                "{method_}"

                - {use1}\n "{metaphor1}"\n This metaphor is describing {word11}. {explain1} {comment1}
                - {use2}\n "{metaphor2}"\n This metaphor is describing {word22}. {explain2} {comment2}
                - {use3}\n "{metaphor3}"\n This metaphor is describing {word33}. {explain3} {comment3}


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


def evaluate(critic):
    r = "\n".join(critic.values())
    p = f"""
        The input information includes some analyses of the reactants, and you need to summarize the results of the analysis and extract corresponding content.
        1. Does the teammate's reaction indicate that the speaker's purpose is successful? (i.e. teammates acknowledge the speaker describing their words)
        2. Does the opponent's reaction indicate that the speaker's purpose is successful? (i.e. the opponent did not guess the word based on the description)
        3. Extract suggestions from the two analyses as comment.

        Output in format:
        rival_successful_recognition_count=*
        teammate_successful_recognition_count=* 
        comment="all the suggestions"

        Among them, * representing the specific number of times.
        
        If you receive two reactions from teammates that acknowledge the metaphor and one reaction from your opponent that they did not understand, then:
        Output sample:
        rival_successful_recognition_count=2
        teammate_successful_recognition_count=0
        comment=1. In order to help teammates make clearer judgments, you should... 2. ...


        # INFORMATION
        {r}

        """
    return p























