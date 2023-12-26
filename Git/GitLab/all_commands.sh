#!/bin/bash

GITLAB_URL="https://gitlab.com"


PROJECT_ID="..."

delete_project() {
    curl --request DELETE "$GITLAB_URL/api/v4/projects/$PROJECT_ID?private_token=$GITLAB_API_TOKEN"
}

SOURCE_PROJECT_ID="..."
TARGET_GROUP_ID="..."
NEW_PROJECT_NAME="..."

migrate_project() {
curl --request PUT "$GITLAB_URL/api/v4/projects/$SOURCE_PROJECT_ID/transfer?namespace=$TARGET_GROUP_ID&private_token=$GITLAB_API_TOKEN"
}

USER_ID="..."
GROUP_PROJECT_ID="..."  
ROLE="..."  #No access (0), Minimal access (5), Guest (10), Reporter (20), Developer (30), Maintainer (40), Owner (50)

add_user() {
curl --request POST "$GITLAB_URL/api/v4/projects/$GROUP_PROJECT_ID/members?private_token=$GITLAB_API_TOKEN" --form "user_id=$USER_ID" --form "access_level=$ROLE"
}

get_branch_list() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/branches"
}

get_merged_branch_list() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/branches?merged=true"
}

get_tags_list() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/tags"
}

PROJECT_ID="..."
ASSIGNEE_ID="..."
ISSUE_TITLE="..."
ISSUE_DESCRIPTION="..."

create_issue() {
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/issues?private_token=$GITLAB_API_TOKEN" \
     --form "title=$ISSUE_TITLE" \
     --form "description=$ISSUE_DESCRIPTION" \
     --form "assignee_ids[]=$ASSIGNEE_ID"
}

get_last_issue_id() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/issues?per_page=1 | jq '.[] | .iid'"
}

PROJECT_ID="..."
BRANCH_NAME="..."
REF="source-branch-name"

create_branch() {
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/branches?branch=$BRANCH_NAME&ref=$REF" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"
}

SOURCE_BRANCH="..."
TARGET_BRANCH="..."  
MERGE_REQUEST_TITLE="..."
MERGE_REQUEST_DESCRIPTION="..."

create_branch_merge_request() {
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/merge_requests?source_branch=$SOURCE_BRANCH&target_branch=$TARGET_BRANCH&title=$MERGE_REQUEST_TITLE&description=$MERGE_REQUEST_DESCRIPTION" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"
}

curl --request POST "https://gitlab.com/api/v4/projects/48383215/merge_requests?source_branch=2-issue2-branch&target_branch=main&title=merge_study&description=merge_study" --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"

SOURCE_BRANCH="..."
TARGET_BRANCH="..."
MERGE_REQUEST_TITLE="..."
MERGE_REQUEST_DESCRIPTION="..."
REMOVE_SOURCE_BRANCH="false"

merge_request_confimration_branch_deletion_opt(){
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/merge_requests" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
     --form "source_branch=$SOURCE_BRANCH" \
     --form "target_branch=$TARGET_BRANCH" \
     --form "title=$MERGE_REQUEST_TITLE" \
     --form "description=$MERGE_REQUEST_DESCRIPTION" \
     --form "remove_source_branch=$REMOVE_SOURCE_BRANCH"
}

TAG_NAME="..."  
COMMIT_SHA="..."

tag_commit() {
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/tags?tag_name=$TAG_NAME&ref=$COMMIT_SHA" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN"
}

users_list() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_URL/api/v4/projects/$PROJECT_ID/members?access_level=$PERMISSION"
}

MERGE_REQUEST_IID="MERGE_REQUEST_IID"

get_comments_from_merge_request() {
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "https://gitlab.com/api/v4/projects/48383215/merge_requests/3/notes"
}

COMMIT_SHA="..."
FILE_PATH="..."
LINE_NUMBER="..."
COMMENT="..."
LINE_TYPE="..." #new or old

add_comment_to_commit(){
curl --request POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/commits/$COMMIT_SHA/comments" \
     --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
     --form "note=$COMMENT" \
     --form "path=$FILE_PATH" \
     --form "line=$LINE_NUMBER" --form "line_type=$LINE_TYPE"
}