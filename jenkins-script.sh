#! /bin/bash -x

exit 0

if [ -z "$EMAIL" ] ; then
    echo '$email is not set'
    exit 1
fi

if [ -z "$ZENDESK_PASS" ] ; then
    echo '$zendesk_pass is not set'
    exit 1
fi

if [ -z "$ZENDESK_URL" ] ; then
    echo '$zendesk_url is not set'
    exit 1
fi

# build the documentation
builds="`cat firstapp/.builds.txt`"
for i in $builds ; do
    tox -e firstapp-$i

    if [ $? -ne 0 ] ; then
        echo "tox $i build failed"
        exit 1
    fi
done

# clone the publish script
git clone https://github.com/dreamhost/zendesk-publish-script.git

if [ $? -ne 0 ] ; then
    echo "could not clone the publishing script"
    exit 1
fi

# create a venv to run the publishing script
virtualenv venv ; . venv/bin/activate ; pip install -r zendesk-publish-script/requirements.txt

if [ $? -ne 0 ] ; then
    echo "Failed to make a virtualenv with the proper modules"
    exit 1
fi

# Get all the files that have changed since the last time the script published
# to zendesk
files="`git diff --name-only $GIT_PREVIOUS_SUCCESSFUL_COMMIT $GIT_COMMIT`"

for file in $files ; do
    if `echo $file | grep -e '^firstapp/source/.*\.rst' > /dev/null` && ! `echo $file | grep -e '.*/index.rst' > /dev/null`; then
        if [ -e "$file" ] ; then
            if `cat .files-to-publish.txt | grep $file > /dev/null` ; then
                # if the file extension is .rst and it is not "index.rst", get the
                # location it built to and publish it to the section specified in the
                # file "section_id.txt" in the rst file's directory
                file_name="`basename $file | sed 's/\.rst$//'`"
                dir="`dirname $file`"
                section_id="`cat ${dir}/section_id.txt`"
                for i in $builds ; do
                    html_file="firstapp/build-${i}/html/${file_name}.html"
                    python zendesk-publish-script/publish.py "$html_file" "$section_id"
                    if [ $? -ne 0 ] ; then
                        exit 1
                    fi
                done
            fi
        fi
    fi
done
