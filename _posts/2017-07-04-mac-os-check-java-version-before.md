---
title: 'Mac OS - Check Java version before running script'
date: 2017-07-04 21:53:00 +01:00
redirect_from:
  - /2017/07/mac-os-check-java-version-before.html
---

I needed to check what version of Java was installed on a Mac before running my program, so with the help of [stackoverflow](https://stackoverflow.com/questions/7334754/correct-way-to-check-java-version-from-bash-script) and a few other resources I pulled together the following bash script which checks to see if the version of Java is greater than 1.8 before continuing.

```bash
# Work out the JAVA version we are working with:
JAVA_VER_MAJOR=""
JAVA_VER_MINOR=""
JAVA_VER_BUILD=""

# Based on: http://stackoverflow.com/a/32026447
for token in $(java -version 2>&1 | grep -i version)
do
    if [[ $token =~ \"([[:digit:]])\.([[:digit:]])\.(.*)\" ]]
    then
        JAVA_VER_MAJOR=${BASH_REMATCH[1]}
        JAVA_VER_MINOR=${BASH_REMATCH[2]}
        JAVA_VER_BUILD=${BASH_REMATCH[3]}
        break
    fi
done

#check version is greater than 1.7 (i.e. at least 1.8)
if [ "$JAVA_VER_MAJOR" -gt "1" ]; then
    echo start your program
elif [ "$JAVA_VER_MINOR" -gt "7" ]; then
    echo start your program
else
    echo ERROR - Java needs to be updated.
    echo Currently installed version is $JAVA_VER_MAJOR.$JAVA_VER_MINOR - 1.8 is required
fi
```
