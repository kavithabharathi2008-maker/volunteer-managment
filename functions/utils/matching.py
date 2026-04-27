def calculate_priority_score(task):
    """
    Calculates a priority score based on urgency and issue type impact.
    Higher score means higher priority.
    """
    # Base urgency (1-5) multiplied by 10
    score = task.urgency_level * 10
    
    # Impact multipliers based on issue type (can be tuned)
    impact_multipliers = {
        'Health': 1.5,
        'Food': 1.4,
        'Shelter': 1.4,
        'Education': 1.2,
        'Environment': 1.1,
        'Other': 1.0
    }
    
    multiplier = impact_multipliers.get(task.issue_type, 1.0)
    final_score = int(score * multiplier)
    return final_score

def match_volunteers_to_task(task, all_volunteers):
    """
    Returns a list of tuples (volunteer, match_score) sorted by score descending.
    Matches based on skills and location proximity (simulated).
    """
    matches = []
    
    # Parse task keywords from title, description, and issue type
    task_keywords = set((task.title + " " + task.description + " " + task.issue_type).lower().split())
    
    for volunteer in all_volunteers:
        score = 0
        
        # Skill matching
        volunteer_skills = [s.strip().lower() for s in volunteer.skills.split(',')]
        
        for skill in volunteer_skills:
            # Simple keyword matching
            for keyword in task_keywords:
                if skill in keyword or keyword in skill:
                    score += 20 # Add 20 points for a skill match
                    break # Count each skill match only once

        # Location matching (simplified: exact city match gets 30 points)
        if task.location.lower().strip() == volunteer.location.lower().strip():
            score += 30
            
        # Base availability score
        if "immediate" in volunteer.availability.lower():
            score += 10
            
        if score > 0:
            matches.append((volunteer, score))
            
    # Sort by highest score
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches
