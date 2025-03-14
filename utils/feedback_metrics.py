def generate_feedback(conversation_history, scenario):
    """Generate feedback based on the entire conversation."""
    user_inputs = [entry["user"] for entry in conversation_history]
    ai_responses = [entry["ai"] for entry in conversation_history]
    
    # Example feedback logic
    clarity_score = min(sum(len(text) for text in user_inputs) / 100, 10)  # Example metric, capped at 10
    persuasiveness_score = min(sum(len(text) for text in ai_responses) / 100, 10)  # Example metric, capped at 10
    
    # Calculate total score (average of clarity and persuasiveness)
    total_score = (clarity_score + persuasiveness_score) / 2
    
    # Points to consider when initiating negotiation
    points_to_consider = f"""
    ### Points to Consider When Initiating Negotiation:
    1. **Preparation**: Research the topic thoroughly. For example, in a {scenario}, understand market rates, company policies, and your own achievements.
    2. **Clear Objectives**: Define what you want to achieve. For instance, in a {scenario}, decide on the exact salary increase or benefits you are seeking.
    3. **Active Listening**: Pay attention to the other party's concerns and respond thoughtfully.
    4. **Flexibility**: Be open to compromise and alternative solutions.
    """
    
    # Detailed performance analysis
    performance_analysis = f"""
    ### Detailed Performance Analysis:
    - **Clarity**: Your clarity score is {clarity_score:.2f}/10. This reflects how clearly you communicated your points.
    - **Persuasiveness**: Your persuasiveness score is {persuasiveness_score:.2f}/10. This reflects how effectively you convinced the other party.
    - **Total Score**: Your overall performance score is {total_score:.2f}/10.
    
    **Areas for Improvement**:
    1. **Be More Concise**: Avoid lengthy explanations. Focus on key points.
    2. **Use Data and Examples**: Support your arguments with data and specific examples.
    3. **Practice Active Listening**: Respond to the other party's concerns more effectively.
    """
    
    feedback = {
        "summary": "You demonstrated good negotiation skills but could improve on clarity and structure.",
        "improvements": [
            "Be more concise in your arguments.",
            "Use data and examples to support your points.",
            "Practice active listening to better understand the other party."
        ],
        "score": {
            "Clarity": clarity_score,
            "Persuasiveness": persuasiveness_score,
            "Total": total_score
        },
        "points_to_consider": points_to_consider,
        "performance_analysis": performance_analysis
    }
    return feedback