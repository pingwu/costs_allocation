# costs_allocation
Costs allocation based on rules defined in flexible Yaml configuration file.

## Problem statement:
- Cloud cost allocation is a complex process heavily dependent on business logic and often involves intricate allocation rules. Many organizations resort to manual allocation using spreadsheets, which is time-consuming and prone to errors.
- While tagging is crucial for effective cloud cost allocation, inconsistent tagging practices and missing tags are common challenges that hinder accurate allocation.
- Automated solutions exist, but they often come with a hefty price tag. Many vendors charge a percentage of monthly cloud spending, which can become increasingly expensive as cloud usage grows.
- This cost allocation solution is versatile and not limited to cloud costs. It can be applied to any numerical values that follow a similar pattern and need to be allocated across different categories.
- Our script provides a flexible, cost-effective alternative that can handle complex allocation rules while maintaining transparency and auditability.

## The Solution:
- Unlock the proprietary intelligent cost allocation tools with this solution that transforms complex rules into auditable automated process.
- The solution efficiently processes your input file, applies sophisticated allocation rules defined in a user-friendly YAML configuration, and produces a detailed output file.
- Our versatile approach handles various scenarios, including:
    - Dynamic relabeling of categories
    - Precise cost adjustments with audit trails
    - Flexible cost distribution, both evenly and proportionally
- For enhanced transparency, the solution generates intermediate files, allowing you to track the allocation process step by step.

## The Benefit:
- The script significantly reduces the time required for cost allocation tasks, improving efficiency.
- It ensures consistency and minimizes errors compared to manual processes.
- The YAML configuration file is human-readable and easily modifiable, allowing for flexible rule adjustments.
- Each month can have its own YAML file, serving as a natural audit trail to explain cost allocation decisions to business leaders.
- This approach enhances transparency and facilitates historical analysis of allocation strategies.

## Usage

```
python cost_management.py [input file name in csv format] [yaml configuration file]

```
## Input file example:

```
category,costs
a1,199
A-1,20
aaa,40
Bx,33
by,77
bb,300
bbb2,200
cook,30
can,82
chair,30
kitchen,50
share,100
school,510
look,29
stove,108
table,10
a1,1
```
### Explanation of input file:
- The first column is the category of the cost.
- The second column is the cost that need to be allocated.

## The Yaml file example:

```
change_label:
  - aaa : aaa2
  - ^bb.* : bbbbb
cost_adjustment:
  - school:
    - [100.33, "because we need to make change here."]
    - [-100.33, "because because change goes here."]
  - share:
    - [100.43, "explain why add 100.43 goes here."]
    - [-100.43: "explain need to know what had happend as comments."]
share_evenly:
  - school:
    - cook
    - look
    - aaa2
share_proportional:
  - share:
      []
  - kitchen:
    - cook  
    - stove
    - table
```

### Explanation of Yaml file:
- change_label:
  - aaa : aaa2
  - ^bb.* : bbbbb
#### This will change all aaa to aaa2 and all bb to bbbbb; the key is the regex pattern and the value is the new value.

- cost_adjustment:
  - school:
    - [100.33, "because we need to make change here."]
    - [-100.33, "because because change goes here."]

#### This will add 100.33 to "school" per example impute file as category.  and subtract -100.33 to school; the second value in the list is the comment for change justification.

- share_evenly:
  - school:
    - cook
    - look
    - aaa2
#### This will allocate the "school" cost evenly to cook, look, and aaa2; the cost will be divided by the number of categories and each category will be added the same value.

- share_proportional:
  - share:
    []

#### This will allocate the "share" cost proportionally to the entire category if the share category list is an empty list in the Yaml file.

  - kitchen:
    - cook  
    - stove
    - table
#### This will allocate the "kitchen" cost proportionally to the listed category in the Yaml file.  The sum of the kitchen cost will be divided by the sum of the cook, stove, and table cost.  Then each category will be multiplied by the result of the sum of the kitchen cost divided by the sum of the cook, stove, and table cost.


## Expected output:

## Expected Output and Benefits:

1. Final Output:
   - The script will generate a CSV file combining the names of the input and YAML files.
   - This output file will be saved in the same directory as the input file.

2. Intermediate Files:
   - The script will create a series of intermediate files in the same directory.
   - These files allow for step-by-step verification of the cost allocation process.

3. Time Efficiency:
   - The script significantly reduces the time required for cost allocation tasks.

4. Consistency and Accuracy:
   - By automating the process, the script ensures more consistent results.
   - It minimizes the risk of human errors in cost allocation calculations.

5. Flexibility and Readability:
   - The YAML file format is human-readable and easily modifiable.
   - Each month can have its own YAML file, providing a clear audit trail.
   - This approach allows for easy explanation of cost allocations to business leaders.

6. Audit Trail:
   - The monthly YAML files serve as a natural historical record.
   - They provide transparency and justification for past cost allocation decisions.


## follow me on www.linkedin.com/in/pingai 
### for any question email to ping@ping-ai.com
### visit us at www.ping-ai.com for Language Model Intelligence Guide newsletter
### visit us at www.ping-ai.com/blog-1 for intelligence articles
### Love to connect and hear from you.


    
