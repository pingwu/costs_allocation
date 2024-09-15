import pandas as pd
import yaml
import sys
import os
import re
from typing import Dict, List, Union

# Ensure costs are stored as two decimal floating numbers
pd.options.display.float_format = '{:.2f}'.format

def output_intermediate_csv(df: pd.DataFrame, step: str):
    """Output intermediate CSV for tracking and debugging purposes."""
    df_with_comments = df.copy()
    if 'comments' not in df_with_comments.columns:
        df_with_comments['comments'] = ''
    output_path = f"intermediate_{step}.csv"
    df_with_comments.to_csv(output_path, index=False)
    print(f"Intermediate CSV saved: {output_path}")


def share_proportional(df: pd.DataFrame, category: str, distribution: List[str]) -> pd.DataFrame:
    comments_name = f"share_proportional_{category}"
    if comments_name not in df.columns:
        df[comments_name] = ''
    
    if category not in df['category'].values:
        raise ValueError(f"Category '{category}' not found in the DataFrame")
    
    cost_to_share = df.loc[df['category'] == category, 'costs'].values[0]
    print(f"category: {category}")
    print(f"Cost to share: {cost_to_share}")
    print(f"Distribution: {distribution}")

    # Check if the category costs have already been distributed
    if cost_to_share == 0:
        df.loc[df['category'] == category, comments_name] += f"{0.00:.2f}"
        return df
    
    # If distribution list is empty, share across all categories except the parent
    if not distribution:
        distribution = df[df['category'] != category]['category'].tolist()
    
    # Calculate total cost of distribution categories
    total_dist_cost = df[df['category'].isin(distribution)]['costs'].sum()
    
    if total_dist_cost == 0:
        # If total cost is 0, share evenly
        share = cost_to_share / len(distribution)
        for sub_category in distribution:
            if sub_category in df['category'].values:
                df.loc[df['category'] == sub_category, 'costs'] += share
                df.loc[df['category'] == sub_category, comments_name] = f"{share:.2f}"
            else:
                new_row = {'category': sub_category, 'costs': share, comments_name: f"{share:.2f}"}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Share proportionally
        for sub_category in distribution:
            if sub_category in df['category'].values:
                sub_cost = df.loc[df['category'] == sub_category, 'costs'].values[0]
                share = (sub_cost / total_dist_cost) * cost_to_share
                df.loc[df['category'] == sub_category, 'costs'] += share
                df.loc[df['category'] == sub_category, comments_name] = f"{share:.2f}"
            else:
                # If sub_category doesn't exist, create it with 0 cost and then share
                new_row = {'category': sub_category, 'costs': 0, comments_name: ''}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                share = 0  # New category gets 0 share as it had 0 initial cost
                df.loc[df['category'] == sub_category, comments_name] += f"New category. Received {share:.2f} from {category} (shared proportionally). "
    
    df.loc[df['category'] == category, comments_name] += f"{-cost_to_share:.2f}"
    df.loc[df['category'] == category, 'costs'] = 0  # Set the original category's cost to 0
    return df

def share_evenly(df: pd.DataFrame, category: str, distribution: List[str]) -> pd.DataFrame:
    comments_name = f"share_evenly_{category}"
    if comments_name not in df.columns:
        df[comments_name] = ''
    
    if category not in df['category'].values:
        raise ValueError(f"Category '{category}' not found in the DataFrame")
    
    cost_to_share = df.loc[df['category'] == category, 'costs'].values[0]
    print(f"category: {category}")
    print(f"Cost to share: {cost_to_share}")
    print(f"Distribution: {distribution}")

    # Check if the category costs have already been distributed
    if cost_to_share == 0:
        df.loc[df['category'] == category, comments_name] += f"Costs for {category} have already been distributed. No further action taken. "
        return df
    
    share = cost_to_share / len(distribution)
    
    for sub_category in distribution:
        if sub_category in df['category'].values:
            df.loc[df['category'] == sub_category, 'costs'] += share
            df.loc[df['category'] == sub_category, comments_name] += f"{share:.2f}"
        else:
            new_row = {'category': sub_category, 'costs': share, comments_name: f"New category. Received {share:.2f} from {category} (shared evenly). "}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    # negative cost to show it was distributed
    df.loc[df['category'] == category, comments_name] += f"-{cost_to_share:.2f}"
    df.loc[df['category'] == category, 'costs'] = 0  # Set the original category's cost to 0
    
    return df

def change_labels(df, label_changes):
    if 'change_labels_ comments' not in df.columns:
        df['change_labels_comments'] = ''
    for pattern, new_label in label_changes:
        mask = df['category'].str.match(pattern)
        # Store original labels and pattern in comments before changing
        df.loc[mask, 'change_labels_comments'] += df.loc[mask, 'category'].apply(lambda x: f"Original: {x}, use regex: {pattern}; ")
        df.loc[mask, 'category'] = new_label
    return df

def get_file_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def share_costs(df, category, distribution):
    cost_to_share = df.loc[df['category'] == category, 'costs'].values[0]
    sub_categories = df[df['category'].isin(distribution)]
    total_sub_cost = sub_categories['costs'].sum()
    
    # Calculate the total cost including the category to be shared
    total_cost = total_sub_cost + cost_to_share
    
    for sub_category in distribution:
        if sub_category not in df['category'].values:
            raise KeyError(f"Category '{sub_category}' not found in input file")
        
        sub_cost = df.loc[df['category'] == sub_category, 'costs'].values[0]
        proportion = sub_cost / total_sub_cost
        share = total_cost * proportion
        df.loc[df['category'] == sub_category, 'costs'] = share
    
    # Remove original category
    df = df[df['category'] != category]
    return df

def cost_adjustment(df, category, adjustments):
    if category not in df['category'].values:
        raise KeyError(f"Category '{category}' not found in input file")
    
    # Create a column for cost adjustment comments if it doesn't exist
    comments_name = f'cost_adjustment_{category}'
    if comments_name not in df.columns:
        df[comments_name] = ''
    
    # Create a column for net adjusted amount if it doesn't exist
    net_adjusted_name = f'net_adjusted_{category}'
    if net_adjusted_name not in df.columns:
        df[net_adjusted_name] = 0.0
    
    print(f"Adjusting category: {category} and adjustments: {adjustments}")
    # Get the original cost before adjustment
    original_cost = df.loc[df['category'] == category, 'costs'].values[0]
    
    # Add the original cost to the comments
    df.loc[df['category'] == category, comments_name] += f"Original cost: {original_cost}; "
    
    total_adjustment = 0.0
    for adjustment in adjustments:
        adjustment_value, comment = adjustment
        adjustment = float(adjustment_value)
        
        # Get the value before change
        value_before_change = df.loc[df['category'] == category, 'costs'].values[0]
        
        # Add the adjustment to the costs of the specified category
        df.loc[df['category'] == category, 'costs'] += adjustment
        
        # Update the net adjusted amount
        total_adjustment += adjustment
        df.loc[df['category'] == category, net_adjusted_name] = total_adjustment
        
        # Add a comment about the adjustment, including the value before change
        adjustment_comment = f"Value before change: {value_before_change:.2f}; Adjusted by {adjustment}: {comment}"
        df.loc[df['category'] == category, comments_name] += adjustment_comment + '; '
    
    # Remove the trailing semicolon and space from comments
    df.loc[df['category'] == category, comments_name] = df.loc[df['category'] == category, comments_name].str.rstrip('; ')
    
    return df


def redistribute_costs(input_file, config_file):
    # Read input CSV, explicitly setting the first row as headers
    df = pd.read_csv(input_file, header=0)
    
    # Check if required columns exist
    required_columns = ['category', 'costs']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in input file: {', '.join(missing_columns)}")

    # Read YAML configuration
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Process each function in the config sequentially
    for function, operations in config.items():
        print(f"Processing function: {function}")
        if function == 'change_label':
            for change in operations:
                for pattern, new_label in change.items():
                    df = change_labels(df, [(pattern, new_label)])
            output_intermediate_csv(df, f"after_change_label")
        elif function == 'cost_adjustment':
            for category_adjustments in operations:
                for category, adjustments in category_adjustments.items():
                    df = cost_adjustment(df, category, adjustments)
            output_intermediate_csv(df, f"after_cost_adjustment")
        elif function == 'share_evenly':
            for category_distribution in operations:
                for category, distribution in category_distribution.items():
                    if category in df['category'].values:
                        df = share_evenly(df, category, distribution)
            output_intermediate_csv(df, f"after_share_evenly")
        elif function == 'share_proportional':
            for category_distribution in operations:
                for category, distribution in category_distribution.items():
                    if category in df['category'].values:
                        df = share_proportional(df, category, distribution)
            output_intermediate_csv(df, f"after_share_proportional")
        elif function == 'regroup':
            if not operations:  # If operations is an empty list
                df = df.groupby('category')['costs'].sum().reset_index()
            else:
                raise Exception("Please check the YAML file. The 'regroup' function should contain an empty list.")
            output_intermediate_csv(df, f"after_regroup")
    # Round costs to three decimal places
    df['costs'] = df['costs'].round(3)
    
    return df

def main(input_file='input.csv', config_file='sharing.yaml'):
    try:
        input_path = get_file_path(input_file)
        config_path = get_file_path(config_file)
        result_df = redistribute_costs(input_path, config_path)
        
        # Generate output filename
        base_name = os.path.splitext(input_file)[0]
        config_name = os.path.splitext(os.path.basename(config_file))[0]
        output_file = f"{base_name}-{config_name}.csv"
        output_path = get_file_path(output_file)
        
        # Write result to CSV
        result_df.to_csv(output_path, index=False)
        print(f"Result written to {output_file}")
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please make sure the input and config files exist in the same directory as the script.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        config_file = sys.argv[2]
        main(input_file, config_file)
    else:
        print("Usage: python cost_management.py [<input_csv> <config_yaml>]")
        print("If no arguments are provided, defaults to input.csv and sharing.yaml")
        sys.exit(1)