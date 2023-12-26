#!/bin/bash

#functions

GITLAB_URL="https://gitlab.com"

# Task a) Create a new project in a specific group
create_project() {
  curl --request POST "$GITLAB_URL/api/v4/projects?private_token=$GITLAB_API_TOKEN" \
     --form "namespace_id=$GROUP_PATH" \
     --form "name=$NEW_PROJECT_NAME"
}

# Task b) Add/delete member, manage project member roles
add_member() {
  curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/members?private_token=$GITLAB_API_TOKEN" \
     --form "user_id=$MEMBER_ID" \
     --form "access_level=$ROLE"
}

del_member() {
  curl --request DELETE "$GITLAB_URL/api/v4/projects/$PROJECT_ID/members/$MEMBER_ID" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"
}

manage_member_role() {
  curl --request PUT "$GITLAB_URL/api/v4/projects/$PROJECT_ID/members/$MEMBER_ID" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
     --data "access_level=$ROLE"
}

# Task c) Manage labels
add_labels() {
  for label in "${labels[@]}"; do
    curl -X POST --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/labels?name=$label&color=green"
  done
}

del_labels() {
  for label in "${labels[@]}"; do
    curl --request DELETE "$GITLAB_URL/api/v4/projects/$PROJECT_ID/labels?name=$label" \
       --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"
  done
}

# Task d) Create an issue
create_issue() {
  
  # Check if the label exists, if not, create it
  label_exists=$(curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/labels?search=$LABEL")
  if [[ -z "$label_exists" ]]; then
    curl -X POST --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/labels?name=$LABEL&color=#FFAABB"
  fi

  # Check if the milestone exists, if not, create it
  milestone_exists=$(curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/milestones?search=$MILESTONE_TITLE")
  if [[ -z "$milestone_exists" ]]; then
    curl -X POST --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/milestones?title=$MILESTONE_TITLE"
  fi

  # Create the issue
  curl -X POST --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/issues?title=$ISSUE_TITLE&description=$DESCRIPTION&assignee_ids[]=$ASSIGNEE_ID&labels=$LABEL&milestone=$MILESTONE_TITLE&due_date=$DUE_DATE"
}

# Task e) Extract problematic lines from merge requests

merge_requests() {
  curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "https://gitlab.com/api/v4/projects/$PROJECT_ID/merge_requests?state=opened"
}

extract_problematic_lines() {
  merge_requests | jq -r '.[] | .iid' | while read -r iid; do
    changes=$(curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "https://gitlab.com/api/v4/projects/$PROJECT_ID/merge_requests/$iid/changes")
    
    date_time=$(echo "$changes" | jq -r '.created_at')
    name_file=$(echo "$changes" | jq -r '.changes | .[] | .new_path')
    number_line=$(echo "$changes" | jq -r '.changes | .[] | .diff')
    author=$(echo "$changes" | jq -r '.author')
    description=$(echo "$changes" | jq -r '.description')
    
    printf "Merge Request IID: %s\n\
date_time: %s\n\
name_file: %s\n\
number_line: %s\n\
author: %s\n\
description: %s\n\
-----------------------------\n" \
"$iid" "$date_time" "$name_file" "$number_line" "$author" "$description"
  done
}

#body

case "$1" in
  "a")
     if [ $# -lt 3 ]; then
          echo "this option needs next arguments after a: group_id project_name"
     else
          GROUP_PATH=$2
          NEW_PROJECT_NAME=$3
          create_project
     fi
    ;;
  "b")
     if [ $2 == "add" ] && [ $# -eq 5 ]; then
          PROJECT_ID=$3
          MEMBER_ID=$4
          ROLE=$5
          add_member
     elif [ $2 == "del" ] && [ $# -eq 4 ]; then           
          PROJECT_ID=$3
          MEMBER_ID=$4
          del_member
     elif [ $2 == "role" ] && [ $# -eq 5 ]; then
          PROJECT_ID=$3
          MEMBER_ID=$4
          ROLE=$5
          manage_member_role
     else
          echo "this option needs next arguments after b: add|role project_id user_id role OR del project_id user_id"
     fi
    ;;
  "c")
     if [ $2 == "add" ] && [ $# -gt 3 ]; then
          PROJECT_ID=$3
          shift 3
          labels=("$@")
          add_labels
     elif [ $2 == "del" ] && [ $# -gt 3 ]; then
          PROJECT_ID=$3
          shift 3
          labels=("$@")
          del_labels
     else
          echo "this option needs next arguments after c: add|del project_id label_1 label_2 ... label_n"
     fi
    ;;
  "d")
     if [ $# -lt 7 ]; then
          echo "this option needs next arguments after d: project_id assignee_id title description label milestone_title due_date(YYYY-MM-DD)"
     else
          PROJECT_ID=$2
          ASSIGNEE_ID=$3
          ISSUE_TITLE=$4
          DESCRIPTION=$5
          LABEL=$6
          MILESTONE_TITLE=$7
          DUE_DATE=$8
          create_issue
     fi
    ;;
  "e")
     if [ $# -lt 2 ]; then
          echo "this option needs next argument after e: project_id"
     else
          PROJECT_ID=$2
          extract_problematic_lines
     fi
    ;;
  *)
     echo "This program requiers specific arguments, use one of the next options: 
  Create new project in group: [a] [group_id] [project_name]
  Add/delete user or manage role: [b] [add|role] [project_id] [user_id] [role] OR [b] [del] [project_id] [user_id]
  Manage labels: [c] [add|del] [project_id] [label_1] [label_2] ... [label_n] 
  Create an issue: [d] [project_id] [assignee_id] [issue_title] [description] [label] [milestone_title] [YYYY-MM-DD]
  Create list of problem line from actual merge requests: [e] [project_id]"
    ;;
esac

