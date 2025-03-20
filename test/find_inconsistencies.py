import sys
import json
import os

# Add the current directory to the path to import hvss_calculator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import hvss_calculator

def calculate_impact_score(vector_string):
    """Calculate the HVSS impact score for a given vector string"""
    # Create a mock event with the vector
    event = {
        'queryStringParameters': {
            'vector': vector_string
        }
    }
    
    # Call the lambda_handler function
    result = hvss_calculator.lambda_handler(event, None)
    
    # Parse the result
    if result['statusCode'] == 200:
        result_data = json.loads(result['body'])
        # Return only the impact score
        return result_data['impact_score']
    else:
        error = json.loads(result['body'])['error']
        raise ValueError(f"Error calculating score: {error}")

def modify_vector(base_vector, metric, value):
    """Safely modify a vector string by replacing a specific metric value"""
    parts = base_vector.split('/')
    
    # Find and replace the metric value
    for i, part in enumerate(parts):
        if part.startswith(f"{metric}:"):
            parts[i] = f"{metric}:{value}"
            break
    
    return '/'.join(parts)

def find_inconsistencies():
    """Find inconsistencies in HVSS score calculations"""
    # Define the vector components and their values in order of increasing restriction/severity
    attack_metrics = {
        "AV": ["N", "A", "L", "P"],  # Network, Adjacent, Local, Physical
        "EAC": ["N", "L", "M", "H", "C", "E"],  # None, Low, Medium, High, Critical, Extreme
        "PR": ["N", "L", "H"],       # None, Low, High
        "UI": ["N", "R"],            # None, Required
    }
    
    # Define impact metrics for each impact type
    impact_metrics = {
        # XCIA impact metrics
        "XCIA": {
            "C": ["N", "L", "H"],    # Confidentiality: None, Low, High
            "I": ["N", "L", "H"],    # Integrity: None, Low, High
            "A": ["N", "L", "H"],    # Availability: None, Low, High
        },
        # XPS impact metrics - Single metric with its values
        "XPS": {
            "XPS": ["N", "L", "MD", "MJ", "C"],  # Privacy: Negligible, Limited, Moderate, Major, Critical
        },
        # XSD impact metrics - Single metric with its values
        "XSD": {
            "XSD": ["N", "SL", "SG", "PL", "PG"],  # Safety/Damage: None, indirect Limited, indirect Substantial, direct Limited, direct substantial
        },
        # XHB impact metrics - Single metric with its values
        "XHB": {
            "XHB": ["N", "DA", "NA", "UI"],  # Hospital Breach: None, Device Availability, Network Access, User Impersonation
        }
    }
    
    # Base vectors for each impact type
    base_vectors = {
        "XCIA": "HVSS:1.0/AV:A/EAC:L/PR:L/UI:N/XIT:XCIA/C:L/I:L/A:L",
        "XPS": "HVSS:1.0/AV:A/EAC:L/PR:L/UI:N/XIT:XPS/XPS:L",
        "XSD": "HVSS:1.0/AV:A/EAC:L/PR:L/UI:N/XIT:XSD/XSD:SL",
        "XHB": "HVSS:1.0/AV:A/EAC:L/PR:L/UI:N/XIT:XHB/XHB:DA"
    }
    
    inconsistencies = []
    
    # Test attack metrics for each impact type
    print("Testing attack metrics (should decrease impact score when restriction increases)...")
    for impact_type, base_vector in base_vectors.items():
        for metric, values in attack_metrics.items():
            for i in range(len(values) - 1):
                less_restrictive = values[i]
                more_restrictive = values[i + 1]
                
                vector1 = modify_vector(base_vector, metric, less_restrictive)
                vector2 = modify_vector(base_vector, metric, more_restrictive)
                
                try:
                    # Calculate impact scores for both vectors
                    imp_score1 = calculate_impact_score(vector1)
                    imp_score2 = calculate_impact_score(vector2)
                    
                    # For attack metrics, impact score should decrease when restriction increases
                    # Only flag as inconsistency if impact score increases or stays the same
                    if imp_score2 >= imp_score1:
                        inconsistencies.append({
                            "type": "attack_metric",
                            "impact_type": impact_type,
                            "metric": metric,
                            "vector1": vector1,
                            "vector2": vector2,
                            "score1": imp_score1,
                            "score2": imp_score2,
                            "change_type": "increase" if imp_score2 > imp_score1 else "same"
                        })
                except Exception as e:
                    print(f"Error testing attack metric {metric} ({less_restrictive} -> {more_restrictive}): {e}")
    
    # Test impact metrics for each impact type
    print("Testing impact metrics (should increase impact score when severity increases)...")
    for impact_type, metrics in impact_metrics.items():
        base_vector = base_vectors[impact_type]
        
        for metric, values in metrics.items():
            for i in range(len(values) - 1):
                less_severe = values[i]
                more_severe = values[i + 1]
                
                vector1 = modify_vector(base_vector, metric, less_severe)
                vector2 = modify_vector(base_vector, metric, more_severe)
                
                try:
                    # Calculate impact scores for both vectors
                    imp_score1 = calculate_impact_score(vector1)
                    imp_score2 = calculate_impact_score(vector2)
                    
                    # For impact metrics, impact score should strictly increase when severity increases
                    if imp_score2 <= imp_score1:
                        inconsistencies.append({
                            "type": "impact_metric",
                            "impact_type": impact_type,
                            "metric": metric,
                            "vector1": vector1,
                            "vector2": vector2,
                            "score1": imp_score1,
                            "score2": imp_score2,
                            "change_type": "same" if imp_score2 == imp_score1 else "decrease"
                        })
                except Exception as e:
                    print(f"Error testing impact metric {metric} ({less_severe} -> {more_severe}): {e}")
    
    return inconsistencies

if __name__ == "__main__":
    print("Finding inconsistencies in HVSS score calculations...")
    try:
        inconsistencies = find_inconsistencies()
        
        if not inconsistencies:
            print("No inconsistencies found!")
        else:
            print(f"\nFound {len(inconsistencies)} inconsistencies:")
            print("-" * 80)
            
            # Print in the requested format
            for i, inc in enumerate(inconsistencies, 1):
                print(f"Inconsistency #{i}:")
                print(f"Vector1: {inc['vector1']}")
                print(f"Vector2: {inc['vector2']}")
                print(f"Score1: {inc['score1']}")
                print(f"Score2: {inc['score2']}")
                
                # Print description based on inconsistency type
                if inc['type'] == 'attack_metric':
                    if inc['change_type'] == 'increase':
                        print(f"Type: Attack metric inconsistency - {inc['metric']} restriction increases but impact score increases")
                    else:  # same
                        print(f"Type: Attack metric inconsistency - {inc['metric']} restriction increases but impact score stays the same")
                    print(f"Impact Type: {inc['impact_type']}")
                elif inc['type'] == 'impact_metric':
                    if inc['change_type'] == 'same':
                        print(f"Type: Impact metric doesn't increase score - {inc['metric']} severity increases but impact score stays the same")
                    else:  # decrease
                        print(f"Type: Impact metric decreases score - {inc['metric']} severity increases but impact score decreases")
                    print(f"Impact Type: {inc['impact_type']}")
                
                print("-" * 80)
            
            # Save results to file
            with open("inconsistencies.txt", "w") as f:
                f.write(f"Found {len(inconsistencies)} inconsistencies:\n\n")
                
                for i, inc in enumerate(inconsistencies, 1):
                    f.write(f"Inconsistency #{i}:\n")
                    f.write(f"Vector1: {inc['vector1']}\n")
                    f.write(f"Vector2: {inc['vector2']}\n")
                    f.write(f"Score1: {inc['score1']}\n")
                    f.write(f"Score2: {inc['score2']}\n")
                    
                    # Write description based on inconsistency type
                    if inc['type'] == 'attack_metric':
                        if inc['change_type'] == 'increase':
                            f.write(f"Type: Attack metric inconsistency - {inc['metric']} restriction increases but impact score increases\n")
                        else:  # same
                            f.write(f"Type: Attack metric inconsistency - {inc['metric']} restriction increases but impact score stays the same\n")
                        f.write(f"Impact Type: {inc['impact_type']}\n")
                    elif inc['type'] == 'impact_metric':
                        if inc['change_type'] == 'same':
                            f.write(f"Type: Impact metric doesn't increase score - {inc['metric']} severity increases but impact score stays the same\n")
                        else:  # decrease
                            f.write(f"Type: Impact metric decreases score - {inc['metric']} severity increases but impact score decreases\n")
                        f.write(f"Impact Type: {inc['impact_type']}\n")
                    
                    f.write("-" * 80 + "\n\n")
            
            print(f"Results saved to inconsistencies.txt")
    except Exception as e:
        print(f"Error: {e}") 