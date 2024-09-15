# costs_allocation
Costs allocation based on Yaml configuration

## Problem statement:
- For cloud costs allocation, it is heavely dependent on the business logic and the allocation rules could be very complicated.  Most likely people are doing this manually and it is error prone using excel or google sheet.
- Tagging hygiene is important for the cloud cost allocation, but most likely the tagging is not done consistently and the tags are not always present.
- If not done manually, they are buying very expensive tools to do this.   Typically the tools vendors charge by the percentage of cloud spendings each month.

## The Solution:
- This script is to solve the problem statement by providing a simple solution to do the costs allocation based on Yaml configuration file.
- The script will read the input file, do the allocation based on the Yaml configuration file, and output the result to a new file.
- It will handle most of the cases:
    - change the label of the category
    - adjust the cost of the category; with one-time adjustment with comment
    - allocate the cost to the category evenly
    - allocate the cost to the category proportionally
- The script will also create a series of intermediate files to verify the result step by step.

## The Benefit:
- The script will save a lot of time for the cost allocation work.
- The script will be more consistent and less error prone.
- The yaml file is human readable and can be easily modified.  Each month can have its own yaml file so when we look back, it is naturally the audit trail to explain the cost allocation to the business leaders.

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

- Final output will be: combine input and yaml file name with csv extension.
- The output file will be in the same directory as the input file.
- It will create a series of intermediate files in the same directory to verify the result step by step.



    
