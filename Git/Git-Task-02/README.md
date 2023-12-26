# m1-Git-Task-02

**PART1**

1.Checkout on ”develop”.

3.Create any file in new folder “task2 –git pracrice II”and commit it.

4.Create new branch “first”.

5.Create another new branch “second”.

6.Do one (or more) commits to “develop” (Add to repository some files, change them).

7.Checkout on the “first” branch and do several commits (about 5).
![Alt text](m-1-pic-task02/1.jpg)

8.Checkout on the “second” branch and do several commits (about 3). Make sure that you have at least one commit, which contains changes in more than one file.
![Alt text](m-1-pic-task02/2.jpg)

9.Do interactive rebasing. Your commits from the “second” branch should appear on the top of “develop” branch.
![Alt text](m-1-pic-task02/3.jpg)

During interactive rebasing: 

• Divide one of your commits (so you should have two commits instead of one) 

![Alt text](m-1-pic-task02/4.jpg)

• Change content of other commit and change commit message for it

![Alt text](m-1-pic-task02/5.jpg)

10.Merge “second” branch into develop(fast-forward).“Develop” and “second” branches should point to the same commit.

![Alt text](m-1-pic-task02/6.jpg)

*Second branch before interactive rebase

![Alt text](m-1-pic-task02/7.jpg)

*Second branch after interactive rebase

![Alt text](m-1-pic-task02/8.jpg)

*Develop branch before merge second

![Alt text](m-1-pic-task02/9.jpg)

*Develop branch after merge second (ff)

![Alt text](m-1-pic-task02/10.jpg)

11.Checkout to the ”first” branch;
12.Do interactive rebasing. Your commits from the “first” branch should appear on the top of “develop” branch. 

![Alt text](m-1-pic-task02/11.jpg)

During interactive rebasing:

• Squash three commits into one; 
• Drop one commit.

![Alt text](m-1-pic-task02/12.jpg)

![Alt text](m-1-pic-task02/13.jpg)

*First branch before rebase develop

![Alt text](m-1-pic-task02/14.jpg)

*First branch after rebase develop

![Alt text](m-1-pic-task02/15.jpg)

*Develop branch before merge first

![Alt text](m-1-pic-task02/16.jpg)

*Develop branch after merge first (ff)

![Alt text](m-1-pic-task02/17.jpg)

14.Merge the “develop” branch into “master” branch.

*Master branch before the last merge develop

![Alt text](m-1-pic-task02/18.jpg)

*Master branch after the last merge develop (no-ff)

![Alt text](m-1-pic-task02/19.jpg)


**ADDITIONAL TASK**

1.Create 4 commits into master branch with minor changes in file that is already exist.

![Alt text](m-1-pic-task02/20.jpg)

2.Execute command git reset--hard HEAD~4 

*After the command execution:*

![Alt text](m-1-pic-task02/21.jpg)

3.Are you able to restore changes of third commit? Describe your steps how to do that.

*Found the commit HEAD@ in the reflog and did cherry-pick, resolved the conflict*

![Alt text](m-1-pic-task02/22.jpg)

*Result:*

![Alt text](m-1-pic-task02/23.jpg)




